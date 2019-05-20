#!/usr/bin/env python3

"""OPC Client that can switch programs on the fly.

Usage:
  multi_opc [options] [<config-file>]
  multi_opc (-h | --help)
  multi_opc --version

Options:
  -d --debug            Log debugging information.
  -h --help             Show this help.
  --version             Show version.

"""

from importlib import import_module
import copy
import json
import logging
import os
import re
import signal
import sys
import threading
import time

from docopt import docopt
import yaml
from watchdog.events import FileSystemEventHandler

from . import color_utils
from . import opc
from ._version import __version__

DEFAULT_CONFIG_FILENAME = "opc.yml"
LOGGER_FORMAT = "%(asctime)-15s %(levelname)s %(name)s - %(message)s"
DEFAULT_LOGGER_LEVEL = logging.INFO
USE_CONFIG_POLLING = (
    True
)  # using polling due to: https://github.com/docker/docker/issues/18246

logger = None
running = True
config_changed = False


class ServerGroup(object):
    """Defines a group of servers that host LED segments of a layout."""

    def __init__(self, name, hosts, layout):
        """Init the server group."""
        self.name = name
        self.hosts = hosts  # {'name': {ip:, port:, start:, end:, power-supply: }}
        self.clients = []  # [(client,start_pixel,end_pixel)...]
        self.layout = layout
        self.source = None
        self.pixels = None  # pixels about to be sent
        self.prev_pixels = None  # last pixels sent
        self.same_pixels_sent_count = 0

    def set_source_class(self, clazz, source_args):
        """Set the plugin class that will generate pixels."""
        if source_args is None:
            source_args = dict()
        self.source = clazz(self.layout, **source_args)

    def connect(self):
        """Connect to configure hosts."""
        logger.info("Setting up %s hosts" % self.name)
        for k, v in self.hosts.items():
            gamma = v.get("gamma")
            client = opc.Client(
                host=v["ip"], port=v["port"], gamma=gamma, verbose=False
            )
            if client.can_connect():
                logger.info(
                    "\tsending to %s:\t(%s:%d)\t[%d-%d] %d"
                    % (
                        k,
                        v["ip"],
                        v["port"],
                        v["start"],
                        v["end"],
                        v["end"] - v["start"] + 1,
                    )
                )
                self.clients.append([client, v["start"], v["end"]])
            else:
                # can't connect, but keep running in case the server appears later
                logger.warn(
                    "\tWARNING: could not connect to {}:{}".format(v["ip"], v["port"])
                )

    def connected(self):
        """Determine if hosts are already connected."""
        return self.client is not None

    def power_use(self, mA_per_pixel):
        """Calculate the approixmate power usage for the currently stored pixels."""
        total_power = 0.0
        for (r, g, b) in self._pixels:
            for i in (r, g, b):
                total_power += abs(i / 255.0) * mA_per_pixel
        return total_power

    def calculate_pixels(self, t):
        """Calculate all pixel values for the current time."""
        if not self.source or not self.clients:
            return
        self.pixels = self.source.all_pixel_colors(t)

    def send_pixels(self):
        """Send the calculated pixels to the hosts."""
        if not self.pixels:
            return
        if self.pixels == self.prev_pixels:
            self.same_pixels_sent_count += 1
        else:
            self.same_pixels_sent_count = 0
        if self.same_pixels_sent_count > 1:
            return

        for client, start_pixel, end_pixel in self.clients:
            if start_pixel == end_pixel == 0:
                # Client gets all pixels
                client.put_pixels(self.pixels, channel=0)
            else:
                # Client gets a subset of pixels
                client.put_pixels(self.pixels[start_pixel : end_pixel + 1], channel=0)
        self.prev_pixels = copy.copy(self.pixels)


class MultiClient(threading.Thread):
    """Multi threaded server for multiple clients."""

    def __init__(self, config):
        """Init from configuration."""
        super().__init__(daemon=True)
        self.__running = True
        self.__config = config
        self.__layouts_dir = config["layouts-directory"]
        self.__plugins_dir = config["plugins-directory"]
        self.__fps = config["fps"]
        self.__plugins = self.__load_plugins()
        self.__server_groups = self.__load_servers()

    def __load_layout(self, layout):
        coordinates = []
        for item in json.load(open(layout)):
            if "point" in item:
                coordinates.append(tuple(item["point"]))
        return coordinates

    def __load_plugins(self):
        logger.info("Loading plugins")
        if self.__plugins_dir not in sys.path:
            sys.path.insert(0, self.__plugins_dir)
        py_re = re.compile(r"^(?!__).*\.py")
        pluginfiles = filter(py_re.search, os.listdir(self.__plugins_dir))
        plugins_map = map(lambda fp: os.path.splitext(fp)[0], pluginfiles)
        # import parent module / namespace
        modules = dict()  # name:module
        for plugin in plugins_map:
            mod = import_module(plugin)
            modules[plugin] = mod
        return modules

    def __load_servers(self):
        logger.debug("Entering loading servers")
        server_groups = dict()
        server_group_names = self.__config["server-groups"].keys()
        logger.debug("Servers in config: %s" % (", ".join(server_group_names)))
        for server_key in server_group_names:
            server_config = self.__config["server-groups"][server_key]
            if not server_config["enable"]:
                continue
            layout_name = server_config["layout"]
            layout = self.__load_layout(
                os.path.join(self.__layouts_dir, layout_name + ".json")
            )
            group = ServerGroup(server_key, server_config["hosts"], layout)
            server_groups[server_key] = group
        logger.debug("Loaded %d servers" % (len(server_groups)))
        return server_groups

    def set_group_class(self, group_name, clazz, source_args):
        """Set the class of a server group."""
        self.__server_groups[group_name].set_source_class(clazz, source_args)

    def get_group_names(self):
        """Get the server group names."""
        return self.__server_groups.keys()

    def __connect_clients(self):
        for group in self.__server_groups.values():
            group.connect()

    def stop(self):
        """Stop running."""
        self.__running = False

    def run(self):
        """Work loop."""
        self.__connect_clients()
        start_time = time.time()
        while self.__running:
            t = time.time() - start_time
            for group in self.__server_groups.values():
                group.calculate_pixels(t)
            for group in self.__server_groups.values():
                group.send_pixels()
            next_frame = start_time + t + (1.0 / self.__fps)
            sleep_time = next_frame - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # warn if it was more than a frame?
                if -sleep_time > (1.0 / self.__fps):
                    logger.warn(
                        "Too much work.  Can't run at request FPS. Over by %d frames "
                        % (-sleep_time / (1.0 / self.__fps))
                    )


def load_scene(scene, multi_client):
    """Load a scene into a multi_client."""
    if not scene:
        logger.warn("Attempted to load an undefined scene")
        return
    for scene_part in scene:
        group_names = scene_part.get("groups")
        source_name = scene_part["source"]
        source_args = scene_part.get("args")
        source_class = color_utils.registered_sources[source_name]
        if group_names is None:
            group_names = multi_client.get_group_names()
        for name in group_names:
            multi_client.set_group_class(name, source_class, source_args)


class ConfigEventHandler(FileSystemEventHandler):
    """Monitor filesystem for configuration changes."""

    def __init__(self, config_file):
        """Init with config file."""
        self.__config_file = config_file
        super()

    def on_modified(self, event):
        """Call back for file modification event."""
        global config_changed
        if event.src_path == self.__config_file:
            logger.warn("Configuration file %s was modified." % self.__config_file)
            config_changed = True


def setup_file_watch(yml_filename):
    """Set up file watcher."""
    event_handler = ConfigEventHandler(yml_filename)
    if USE_CONFIG_POLLING:
        from watchdog.observers.polling import PollingObserver

        observer = PollingObserver()
    else:
        from watchdog.observers import Observer

        observer = Observer()
    parent_dir = os.path.dirname(yml_filename)
    observer.schedule(event_handler, parent_dir, recursive=False)
    observer.start()
    return observer


def setup_logging(debug=False):
    """Set up logging."""
    if debug:
        level = logging.DEBUG
    else:
        level = DEFAULT_LOGGER_LEVEL
    LOGGER_FORMAT = "%(asctime)-15s %(levelname)s %(name)s - %(message)s"
    formatter = logging.Formatter(LOGGER_FORMAT)
    formatter.converter = time.gmtime  # log times in UTC
    root = logging.getLogger()
    root.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    root.debug("Debug logging enabled")
    return root


def shutdown_handler(signum, frame):
    """Handle shutdown signal."""
    logger.warn("Signal handler called with signal %d" % signum)
    global running
    running = False


def reload_handler(signum, frame):
    """Handle reload signal."""
    global config_changed
    logger.warn("Signal handler called with signal %d" % signum)
    logger.info("Reloading config...")
    config_changed = True


def load_config(filename):
    """Load configuration from file."""
    logger.info("Reading configuration from %s" % filename)
    stream = open(filename, "r")
    y = yaml.safe_load(stream)
    return y


def do_work(config):
    """Work loop."""
    global running
    multi_client = MultiClient(config)
    startup_scene = config["scenes"]["startup"]
    # import IPython; IPython.embed() #<<< BREAKPOINT >>>
    load_scene(startup_scene, multi_client)
    multi_client.start()
    while running and not config_changed:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logger.warn("Shutting down due to keyboard interrupt.")
            running = False
    if not running:  # shutting down
        load_scene(config["scenes"]["shutdown"], multi_client)
        time.sleep(0.5)
    logger.debug("Stopping multi client thread")
    multi_client.stop()
    logger.debug("Joining multi client thread")
    multi_client.join()


def main():
    """Start of Multi OPC program."""
    global logger, config_changed, running
    args = docopt(__doc__, version=__version__)
    logger = setup_logging(args["--debug"])
    signal.signal(signal.SIGINT | signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGHUP, reload_handler)
    yml_filename = os.environ.get("OPC_YML", "./opc.yml")
    logger.info(
        "Registered pixel sources: " + ", ".join(color_utils.registered_sources.keys())
    )
    observer = setup_file_watch(yml_filename)
    while running:
        config_changed = False
        config = load_config(yml_filename)
        do_work(config)
    logger.debug("Stopping file observer thread")
    observer.stop()
    logger.debug("Joining file observer thread")
    observer.join()
    logger.warn("Exiting")
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""OPCU Server for Raspberry Pi."""
import socket
import collections
from enum import Enum
import argparse
import math
import signal

DEFAULT_MAX_LEDS = 512
DEFAULT_UDP_PORT = 7890
DEFAULT_SPIDEV_BUS = 0
DEFAULT_SPIDEV_DEVICE = 0
SPIDEV = "/dev/spidev%d.%d"
SPIDEV_SPEED = 25_000_000
GAMMA = 1.5  # 2.5 = Dark, 0.5 = Bright


class StreamMode(Enum):
    """Stream mode enumeration."""

    HEADER = 0
    DATA = 1


class LEDStrip(object):
    """Represents a connect LED strip."""

    def __init__(self, led_count, dev):
        """Init strip with count and output device."""
        self.__dev = dev
        self._led_count = led_count
        self._spidev = open(self.__dev, "wb")
        self.buffer = bytearray(led_count * 3)

    def send(self, size=None):
        """Abstract function to send data to strip."""
        pass


class APA102(LEDStrip):
    """Sender for APA102 (DotStar).

    Pixels over SPI are sent in BGR order.
    Start frame 32-bits:
        32-bits: 0
    LED Frame 32-bits:
        3-bit: 111
        5-bit: Global brightness
        8-bit: Blue
        8-bit: green
        8-bit: red
    End frame 32-bits (not used?):
        32-bits: 1
    """

    def __init__(self, led_count, dev):
        """Init strip with count and output device."""
        super().__init__(led_count, dev)
        self.__start_frame = bytes(b"\x00\x00\x00\x00")
        # end frame of 1 bit per 2 LEDs (rounded to next byte boundary, for SPI).
        end_frame_length = math.ceil((led_count / 2 + 7) / 8)
        self.__end_frame = bytes(b"\xff" * end_frame_length)

    def send(self, size):
        """Send data to strip."""
        self._spidev.write(self.__start_frame)
        i = iter(self.buffer)
        for x in range(0, size, 3):
            r, g, b = bytes([next(i)]), bytes([next(i)]), bytes([next(i)])
            self._spidev.write(b"\xff")  # 111 + global brightness
            self._spidev.write(b)
            self._spidev.write(g)
            self._spidev.write(r)
        self._spidev.write(self.__end_frame)
        self._spidev.flush()


class LPD8806(LEDStrip):
    """LPD8806 Chipset (Shelves).

    Pixels over SPI are send in GRB order.
    """

    def __init__(self, led_count, dev):
        """Init strip with count and output device."""
        super().__init__(led_count, dev)
        self.__end_frame = bytes(b"\x00\x00\x00")
        self.__gamma = self.__adafruit_gamma()
        self.__gamma_applied_buffer = bytearray(led_count * 3)

    def send(self, size):
        """Send data to strip."""
        self.__apply_gamma(int(size / 3))
        self._spidev.write(self.__gamma_applied_buffer[0 : size - 1])
        self._spidev.write(self.__end_frame)
        self._spidev.flush()

    def __apply_gamma(self, size):
        """Apply a gamma to values in ba_in and sets values in ba_out.

        Re-arranges colors to be RGB order.
        """
        for i in range(size):
            self.__gamma_applied_buffer[i * 3 + 0] = self.__gamma[
                self.buffer[i * 3 + 1]
            ]
            self.__gamma_applied_buffer[i * 3 + 1] = self.__gamma[
                self.buffer[i * 3 + 0]
            ]
            self.__gamma_applied_buffer[i * 3 + 2] = self.__gamma[
                self.buffer[i * 3 + 2]
            ]

    def __adafruit_gamma(self):
        """Return the gamma table used in adafruit examples."""
        gamma = bytearray(256)
        for i in range(256):
            gamma[i] = 0x80 | int(pow(float(i) / 255, GAMMA) * 127.0 + 0.5)
        return gamma


def punch_it_chewie(bus, device):
    """Kick the SPI bus into overdrive."""
    try:
        import spidev

        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = SPIDEV_SPEED
    except Exception as e:
        print(e)
        print("Install py-spidev to boost SPI bus speeds.")


def shutdown_handler(signum, frame):
    """Handle shutdown signal."""
    print("Signal handler called with signal", signum)
    global running
    running = False


def noop_handler(signum, frame):
    """Noop handler."""
    print("Signal handler called with signal", signum)
    print("Reloading config... just kidding.")


running = True


def main():
    """Program main entrypoint."""
    signal.signal(signal.SIGINT | signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGHUP, noop_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "protocol", type=str, choices=["apa102", "lpd8806"], help="led strip protocol"
    )
    # parser.add_argument('spidev', type=str, help='Serial Peripheral Interface bus device')
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-6", "--ipv6", help="listen on ipv6 ports", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_UDP_PORT,
        help="port on which to listen",
    )
    parser.add_argument(
        "-b", "--bus", type=int, default=DEFAULT_SPIDEV_BUS, help="spi bus number"
    )
    parser.add_argument(
        "-d",
        "--device",
        type=int,
        default=DEFAULT_SPIDEV_DEVICE,
        help="spi device number",
    )
    parser.add_argument(
        "-m",
        "--max-led-count",
        type=int,
        help="Maximum number of LEDs on the strip",
        default=DEFAULT_MAX_LEDS,
    )

    args = parser.parse_args()
    spi_device = SPIDEV % (args.bus, args.device)
    punch_it_chewie(args.bus, args.device)

    if args.ipv6:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)  # Internet  # UDP
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
        UDP_IP = "::"
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        UDP_IP = "0.0.0.0"  # nosec
    sock.bind((UDP_IP, args.port))

    if args.protocol == "apa102":
        strip = APA102(args.max_led_count, spi_device)
    elif args.protocol == "lpd8806":
        strip = LPD8806(args.max_led_count, spi_device)
    else:
        raise ValueError("Unknown protocol specified: %s" % args.protocol)

    mode = StreamMode.HEADER
    queue = collections.deque(maxlen=4096)
    h_channel, h_command, h_length_hi, h_length_lo = 0, 0, 0, 0
    pixel_data_length = 0

    print("Starting loop writing to: %s" % spi_device)
    while running:
        try:
            data, addr = sock.recvfrom(args.max_led_count * 3 * 2)
        except InterruptedError:
            continue
        if args.verbose:
            print("received message from {}: {}".format(addr, data))
        queue.extend(data)  # add data to end of our queue
        if mode == StreamMode.HEADER:
            if len(queue) < 4:
                continue  # don't have the entire header yet
            h_channel = queue.popleft()
            h_command = queue.popleft()
            h_length_hi = queue.popleft()
            h_length_lo = queue.popleft()
            pixel_data_length = (h_length_hi * 256) + h_length_lo
            if args.verbose:
                print(
                    "got header: {} {} {} {} ({})".format(
                        h_channel,
                        h_command,
                        h_length_hi,
                        h_length_lo,
                        pixel_data_length,
                    )
                )
            mode = StreamMode.DATA
        if mode == StreamMode.DATA:
            if len(queue) < pixel_data_length:
                continue  # don't have all pixel data yet
            if args.verbose:
                print("got data: %d" % pixel_data_length)
            for i in range(pixel_data_length):
                strip.buffer[i] = queue.popleft()
            strip.send(pixel_data_length)
            if len(queue) != 0:
                print("extra data: %d" % len(queue))
                queue.clear()
            mode = StreamMode.HEADER
        # import IPython; IPython.embed() #<<< BREAKPOINT >>>
    # shutdown
    print("Shutting down")
    for i in range(pixel_data_length):
        strip.buffer[i] = 0
    strip.send(pixel_data_length)


if __name__ == "__main__":
    main()

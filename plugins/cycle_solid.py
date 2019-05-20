"""CycleSolid plugin."""

from opc import color_utils
import random
import colorsys
from functools import lru_cache


@color_utils.pixel_source
class CycleSolid(color_utils.PixelGenerator):
    """CycleSolid generator."""

    def __init__(self, layout, tempo=120, hsv_colors=None, rgb_colors=None, seed=0):
        """Init generator with layout."""
        super().__init__(layout)
        self.tempo = tempo
        self.seed = seed
        if hsv_colors:
            self.rgb_colors = [colorsys.hsv_to_rgb(*x) for x in hsv_colors]
        else:
            self.rgb_colors = rgb_colors

    @lru_cache(maxsize=16)
    def get_random_color_for_time(self, t):
        """Get a random color for time."""
        random.seed(t + self.seed)
        hue = random.random()  # nosec
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (r, g, b)

    @lru_cache(maxsize=16)
    def get_color_for_time(self, t):
        """Get a color directly cycled by time."""
        r, g, b = self.rgb_colors[t % len(self.rgb_colors)]
        return (r, g, b)

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels

        Returns an (r, g, b) tuple in the range 0-255

        """
        x, y, z = self._layout[ii]

        if self.rgb_colors:
            r, g, b = self.get_color_for_time(int(t * self.tempo / 60.0))
        else:
            r, g, b = self.get_random_color_for_time(int(t * self.tempo / 60.0))

        return (r, g, b)

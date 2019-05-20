"""RainbowShelves generator."""
from opc import color_utils
import random
import colorsys
from functools import lru_cache


@color_utils.pixel_source
class RainbowShelves(color_utils.PixelGenerator):
    """RainbowShelves generator."""

    def __init__(self, layout, block_size=18, seed=0):
        """Init generator with layout."""
        super().__init__(layout)
        self.seed = seed
        self.block_size = block_size

    @lru_cache(maxsize=16)
    def get_random_color_for_time(self, t, shelf):
        """Get a color for the current time."""
        random.seed(t + self.seed + shelf)
        hue = random.random()  # nosec
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
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
        r = g = b = 0
        div_t = int(t) / 4

        shelf = int(ii / self.block_size)
        r, g, b = self.get_random_color_for_time(div_t, shelf)

        return (r, g, b)

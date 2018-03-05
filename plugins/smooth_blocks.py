from opc import color_utils
import random
import colorsys
from functools import lru_cache

@color_utils.pixel_source
class SmoothBlocks(color_utils.PixelGenerator):
    def __init__(self, layout, block_size=18, seed=0):
        super().__init__(layout)
        self.seed = seed
        self.block_size = block_size

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels

        Returns an (r, g, b) tuple in the range 0-255

        """
        x, y, z = self._layout[ii]

        block = int(ii / self.block_size)
        period = (((block + 1) * 51) % 37) + 1

        hue = color_utils.cos(t/25 + block, offset=0, period=period, minn=0.0, maxx=1.0)
        r,g,b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        return (r, g, b)

from opc import color_utils
import random

@color_utils.pixel_source
class Strobe(color_utils.PixelGenerator):
    def __init__(self, layout):
        self.count = 0
        super().__init__(layout)

    def all_pixel_colors(self, t):
        '''Compute the color of all the pixels.'''
        p = self.pixel_color(t, 0)
        n_pixels = len(self._layout)
        self._pixels = [p] * n_pixels
        return self._pixels

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels

        Returns an (r, g, b) tuple in the range 0-255

        """
        #c = color_utils.cos(t, offset=0, period=0.3, minn=0, maxx=1)
        self.count += 1
        #if c > 0.95:
        if self.count > 10:
            self.count = 0
            return (1,1,1)
        return (0,0,0)

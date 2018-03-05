from opc import color_utils
import random

@color_utils.pixel_source
class Water(color_utils.PixelGenerator):
    def __init__(self, layout):
        super().__init__(layout)

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels

        Returns an (r, g, b) tuple in the range 0-255

        """
        x, y, z = self._layout[ii]

        w1 = color_utils.cos(t, period=17)
        w2 = color_utils.cos(t, offset=30, period=23)
        #r = g = b = color_utils.cos(x+y, offset=w1, period=1, minn=0.0, maxx=0.4)
        #(r,g,b) = color_utils.contrast((r,g,b), 0.5, 4)
        r = 0
        b = color_utils.cos(x+y, offset=w1, period=5, minn=0.1, maxx=0.5)
        g = color_utils.cos(x+y, offset=w2, period=3, minn=0.2, maxx=0.4)
        return (r, g, b)

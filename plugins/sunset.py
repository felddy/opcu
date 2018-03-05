from opc import color_utils
import random

@color_utils.pixel_source
class Sunset(color_utils.PixelGenerator):
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

        darkblue = (0.0, 0.0, 0.0)
        orange = (0.5, 0.25, 0.0)
        red = (0.8, 0.0, 0.0)
        yellow = (0.7, 0.7, 0.0)

        orange_ch = color_utils.scale(orange, color_utils.cos(x+y, offset=-w2, period=3, minn=0.1, maxx=0.5))
        yellow_ch = color_utils.scale(yellow, color_utils.cos(x+y, offset=w1, period=5, minn=0.1, maxx=0.5))
        red_ch = color_utils.scale(red, color_utils.cos(x+y, offset=w2, period=7, minn=0.2, maxx=0.4))

        r,g,b = darkblue
        r,g,b = color_utils.v_add([r,g,b], orange_ch)
        r,g,b = color_utils.v_add([r,g,b], yellow_ch)
        r,g,b = color_utils.v_add([r,g,b], red_ch)

        return (r, g, b)

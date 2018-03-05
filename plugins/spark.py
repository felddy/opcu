from opc import color_utils
import random

@color_utils.pixel_source
class Spark(color_utils.PixelGenerator):
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
        r = g = b = 0
        # make a moving white dot showing the order of the pixels in the layout file
        spark_ii = (t*80) % self.n_pixels()
        spark_rad = 16
        spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, self.n_pixels())) / spark_rad)
        spark_val = min(1, spark_val*2)
        r += spark_val
        g += spark_val
        b += spark_val

        return (r, g, b)

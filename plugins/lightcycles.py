"""Generate light cycle effect."""
from opc import color_utils


@color_utils.pixel_source
class LightCycles(color_utils.PixelGenerator):
    """Generate light cycle effect."""

    def __init__(self, layout):
        """Init generator with layout."""
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
        spark_ii = int((t * 80) % self.n_pixels())
        # spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, self.n_pixels())) / spark_rad)
        spark_val = 1.0 if ii == spark_ii else 0.0
        # spark_val = min(1, spark_val*2)
        r += spark_val
        g += spark_val
        b += spark_val

        return (r, g, b)

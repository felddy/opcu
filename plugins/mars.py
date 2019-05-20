"""Mars generator."""
from opc import color_utils


@color_utils.pixel_source
class Mars(color_utils.PixelGenerator):
    """Mars generator."""

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
        x, y, z = self._layout[ii]

        w1 = color_utils.cos(t, period=17)
        w2 = color_utils.cos(t, offset=30, period=23)

        red = (1.0, 0.0, 0.0)
        orange = (0.5, 0.25, 0.0)

        channel_1 = color_utils.scale(
            red, color_utils.cos(x + y, offset=-w2, period=3, minn=0.1, maxx=0.5)
        )
        channel_2 = color_utils.scale(
            orange, color_utils.cos(x + y, offset=w1, period=5, minn=0.1, maxx=0.5)
        )

        r, g, b = (0, 0, 0)
        r, g, b = color_utils.v_add([r, g, b], channel_1)
        r, g, b = color_utils.v_add([r, g, b], channel_2)

        return (r, g, b)

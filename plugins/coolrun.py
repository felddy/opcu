"""Coolrun plugin."""
from opc import color_utils


@color_utils.pixel_source
class CoolRun(color_utils.PixelGenerator):
    """CoolRun generator."""

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

        darkblue = (0.0, 0.0, 0.0)
        # blue = (0.0, 0.0, 1.0)
        magenta = (1.0, 0.0, 1.0)
        cyan = (0.0, 0.7, 0.7)

        # channel_1 = color_utils.scale(
        #     blue, color_utils.cos(x + y, offset=-w2, period=3, minn=0.1, maxx=0.5)
        # )
        channel_2 = color_utils.scale(
            magenta, color_utils.cos(x + y, offset=w1, period=5, minn=0.1, maxx=0.5)
        )
        channel_3 = color_utils.scale(
            cyan, color_utils.cos(x + y, offset=w2, period=7, minn=0.2, maxx=0.4)
        )

        r, g, b = darkblue
        # r,g,b = color_utils.v_add([r,g,b], channel_1)
        r, g, b = color_utils.v_add([r, g, b], channel_2)
        r, g, b = color_utils.v_add([r, g, b], channel_3)

        return (r, g, b)

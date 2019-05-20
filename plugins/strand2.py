"""Strand plugin."""
from opc import color_utils
import colorsys


@color_utils.pixel_source
class Strand2(color_utils.PixelGenerator):
    """Strand generator."""

    def __init__(
        self, layout, hsv_colors=None, rgb_colors=None, grouping=1, spacing=10
    ):
        """Intilize generator."""
        self.grouping = grouping
        self.spacing = spacing
        if hsv_colors:
            self.rgb_colors = [colorsys.hsv_to_rgb(*x) for x in hsv_colors]
        else:
            self.rgb_colors = rgb_colors
        if not self.rgb_colors:
            self.rgb_colors = (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
                (1.0, 1.0, 0),
            )
        self.lookup = self.gen_strand()
        super().__init__(layout)

    def gen_strand(self):
        """Calculate the layout of a single interval."""
        lookup = list()
        color_count = len(self.rgb_colors)
        self.spacing = max(self.spacing, color_count)  # prevent foot shooting
        step = int(self.spacing / color_count)
        color_it = iter(self.rgb_colors)
        for i in range(self.spacing):
            if i % step == 0:
                try:
                    lookup.append(next(color_it))
                except StopIteration:
                    lookup.append((0.0, 0.0, 0.0))
            else:
                lookup.append((0.0, 0.0, 0.0))
        return lookup

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels

        Returns an (r, g, b) tuple in the range 0-255

        """
        # x, y, z = self._layout[ii]
        r = g = b = 0

        blinker = color_utils.cos(ii / 100, offset=t / 8, period=1, minn=0.0, maxx=1.0)

        if blinker < 0.5:
            return (0, 0, 0)

        m = int(ii / self.grouping) % self.spacing

        if int(t) % 4 > 1:
            m = (m + self.spacing // 2) % self.spacing
        return self.lookup[m]

        return (r, g, b)

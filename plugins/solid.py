"""Solid plugin."""
from opc import color_utils
import colorsys


@color_utils.pixel_source
class Solid(color_utils.PixelGenerator):
    """Solid generator."""

    def __init__(self, layout, rgb=None, hsv=None):
        """Init generator with layout."""
        super().__init__(layout)
        if rgb:
            self.rgb = rgb
        elif hsv:
            self.rgb = colorsys.hsv_to_rgb(*hsv)
        else:
            self.rgb = (0, 0, 0)

    def pixel_color(self, t, ii):
        """Return the solid color."""
        return self.rgb

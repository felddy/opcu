from opc import color_utils
import random
import colorsys

@color_utils.pixel_source
class Solid(color_utils.PixelGenerator):
    def __init__(self, layout, rgb=None, hsv=None):
        super().__init__(layout)
        if rgb:
            self.rgb = rgb
        elif hsv:
            self.rgb = colorsys.hsv_to_rgb(*hsv)
        else:
            self.rgb = (0,0,0)

    def pixel_color(self, t, ii):
        return self.rgb

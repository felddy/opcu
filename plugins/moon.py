from opc import color_utils
import random

@color_utils.pixel_source
class SailorMoon(color_utils.PixelGenerator):
    def __init__(self, layout):
        super().__init__(layout)
        self.__random_values = [random.random() for ii in range(len(layout))]
        self.__twinkle_speed = 0.07
        self.__twinkle_density = 0.1

    def pixel_color(self, t, ii):
        """Compute the color of a given pixel.

        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple

        Returns an (r, g, b) tuple in the range 0-255

        """

    #     # random persistant color per pixel
    #     r = color_utils.remap(random_values[(ii+0)%n_pixels], 0, 1, 0.2, 1)
    #     g = color_utils.remap(random_values[(ii+3)%n_pixels], 0, 1, 0.2, 1)
    #     b = color_utils.remap(random_values[(ii+6)%n_pixels], 0, 1, 0.2, 1)

        # random assortment of a few colors per pixel: pink, cyan, white
        if self.__random_values[ii] < 0.5:
            r, g, b = (1, 0.3, 0.8)
        elif self.__random_values[ii] < 0.85:
            r, g, b = (0.4, 0.7, 1)
        else:
            r, g, b = (2, 0.6, 1.6)

        # twinkle occasional LEDs
        twinkle = (self.__random_values[ii]*7 + t*self.__twinkle_speed) % 1
        twinkle = abs(twinkle*2 - 1)
        twinkle = color_utils.remap(twinkle, 0, 1, -1/self.__twinkle_density, 1.1)
        twinkle = color_utils.clamp(twinkle, -0.5, 1.1)
        twinkle **= 5
        twinkle *= color_utils.cos(t - ii/self.n_pixels(), offset=0, period=7, minn=0.1, maxx=1.0) ** 20
        twinkle = color_utils.clamp(twinkle, -0.3, 1)
        r *= twinkle
        g *= twinkle
        b *= twinkle

        return (r, g, b)

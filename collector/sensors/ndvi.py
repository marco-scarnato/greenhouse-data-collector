import cv2
import numpy as np
from picamera2 import Picamera2


class NDVI:
    def __init__(self, format: str = "RGB888") -> None:
        """Initializes the camera, a config can be passed as a dictionary

        Args:
            # TODO what is the config parameter? Is this a typo?
            config (str, optional): refer to https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
            for all possible values, the default is RGB888 which is mapped to an array of pixels [B,G,R].
            Defaults to "RGB888".

            transform (libcamera.Transform, optional): useful to flip the camera if needed.
            Defaults to Transform(vflip=True).
        """

        self.camera = Picamera2()
        self.camera.still_configuration.main.format = format
        self.camera.configure("still")
        self.camera.start()

    def contrast_stretch(self, image):
        """Increases contrast of image to facilitate NDVI calculation"""

        # Find the top 5% and bottom 5% of pixel values
        in_min = np.percentile(image, 5)
        in_max = np.percentile(image, 95)

        # Defines minimum and maximum brightness values
        out_min = 0
        out_max = 255

        out = image - in_min
        out *= (out_min - out_max) / (in_min - in_max)
        out += in_min

        return out

    def calculate_ndvi(self, image):
        b, g, r = cv2.split(image)
        bottom = r.astype(float) + b.astype(float)
        bottom[bottom == 0] = 0.01  # Make sure we don't divide by zero!
        ndvi = (r.astype(float) - b) / bottom

        return ndvi

    def read(self):
        # TODO: check if there are more accurate ways to compute the number representing the plant health
        return np.mean(
            self.calculate_ndvi(self.contrast_stretch(self.camera.capture_array()))
        )

    def stop(self):
        self.camera.stop()
        self.camera.close()

import cv2
from time import sleep


class LightLevel:
    """
    Approximate light level reding using a webcam and OpenCV
    """

    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        sleep(2)  # lets webcam adjust its exposure
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)

    def read(self):
        ret, frame = self.cap.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_light_level = cv2.mean(grey)[0]
        return avg_light_level

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

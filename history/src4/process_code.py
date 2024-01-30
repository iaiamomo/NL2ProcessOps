from tools.CaptureImage import CaptureImage
from tools.CheckMarkers import CheckMarkers
from tools.SetSpeed import SetSpeed

def calibration_process():
    while True:
        image = CaptureImage.call()
        markers_ok = CheckMarkers.call(image=image)
        if markers_ok:
            SetSpeed.call(speed=10000)
            break

if __name__ == '__main__':
	calibration_process()
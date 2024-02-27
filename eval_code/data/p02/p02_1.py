from tools.camera import CaptureImage
from tools.vision_is import CheckMarkers
from tools.die_machine import SetSpeedDieMachine

def process():
    while True:
        image = CaptureImage.call()
        markers_ok = CheckMarkers.call(image=image)
        if markers_ok:
            SetSpeedDieMachine.call(speed=10000)
            break

if __name__ == "__main__":
    process()
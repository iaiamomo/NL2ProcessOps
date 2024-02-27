from tools.worker import CheckTypeCardboard, InsertCardboardTypeInfo, StoreCardboardRoll
from tools.camera import CaptureImage
from tools.vision_is import AnalyzeWarehouse
from tools.wms_is import UpdateStock


def process():
    cardboard_type = CheckTypeCardboard.call()

    InsertCardboardTypeInfo.call(cardboard_type)

    image = CaptureImage.call()

    location = AnalyzeWarehouse.call(image)

    StoreCardboardRoll.call(location)

    UpdateStock.call(cardboard_type)

if __name__ == '__main__':
    process()
from vision_is import AnalyzeWarehouse
from worker import CheckTypeCardboard, StoreCardboardRoll
from wms_is import UpdateStock

def process_new_cardboard_roll(image: np.matrix):
    # Worker checks the type of cardboard
    type_cardboard = CheckTypeCardboard().call()

    # System identifies the location where the cardboard roll should be stored
    location = AnalyzeWarehouse().call(image, type_cardboard)

    # Worker stores the cardboard roll in the identified location
    StoreCardboardRoll().call(location)

    # System updates the stock of that cardboard rolls in the warehouse
    UpdateStock().call(type_cardboard)
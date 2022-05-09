import threading
from general_state import GeneralState


class General(threading.Thread):
    def __init__(self, id: int, is_primary: bool):
        super().__init__()
        self.id = id
        self.state = GeneralState.NON_FAULTY
        self.primary = is_primary

    def role(self) -> str:
        if self.primary:
            return "primary"
        else:
            return "secondary"

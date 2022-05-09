from enum import Enum

class GeneralState(Enum):
    FAULTY = "F"
    NON_FAULTY = "NF"

    def __str__(self):
        return self.value
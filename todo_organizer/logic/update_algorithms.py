from enum import Enum


class UpdateAlgorithms(Enum):
    No = 0
    Increment = 1
    Date = 2

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

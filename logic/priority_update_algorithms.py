from enum import Enum


class PriorityUpdateAlgorithms(Enum):
    No = 0
    Increment = 1

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

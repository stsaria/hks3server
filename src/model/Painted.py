from dataclasses import dataclass

from src.defined import SKETCH_RANGE

class CoordinatesOutOfRange(Exception):
    pass

class ColorsOutOfRange(Exception):
    pass

def isNotOkRange(a:int) -> bool:
    return a > SKETCH_RANGE[0] or a < 0

@dataclass
class Painted:
    timestamp:int
    x:int
    y:int
    r:int
    g:int
    b:int

    def __post_init__(self):
        def isNORangeC(a:int) -> bool:
            return a > 255 or a < 0
        if self.x > SKETCH_RANGE[0] or self.y > SKETCH_RANGE[1] or self.x < 0 or self.y < 0:
            raise CoordinatesOutOfRange()
        elif isNORangeC(self.r) or isNORangeC(self.g) or isNORangeC(self.b):
            raise ColorsOutOfRange()

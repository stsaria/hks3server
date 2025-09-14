from dataclasses import dataclass

from src.defined import SKETCH_RANGE

class CoordinatesIsOutOfRange(Exception):
    pass

class ColorIsOutOfRange(Exception):
    pass

def isNotOkRange(a:int) -> bool:
    return a > SKETCH_RANGE[0] or a < 0

@dataclass
class Painted:
    ip:str
    x:int
    y:int
    r:int
    g:int
    b:int

    def __post_init__(self):
        def isNORange(a:int) -> bool:
            return a > SKETCH_RANGE[0] or a < 0
        def isNORangeC(a:int) -> bool:
            return a > 255 or a < 0
        if isNORange(self.x) or isNotOkRange(self.y):
            raise CoordinatesIsOutOfRange()
        elif isNORangeC(self.r) or isNORangeC(self.g) or isNORangeC(self.b):
            raise ColorIsOutOfRange()

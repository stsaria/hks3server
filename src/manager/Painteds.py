from threading import RLock
import time

from src.defined import FIRST_RIGHTS, MAX_RIGHTS, RIGHT_ACQUIRE_WAIT_SEC
from src.model.Painted import Painted

COLOR = tuple[int, int, int]

class YouDontHaveRights(Exception):
    pass

class Painteds:
    _ipAndPaintedsS:dict[str:list[Painted]] = {}
    _ipAndPaintedsSLock = RLock()

    @classmethod
    def _getLogsByIp(cls, ip:str) -> list[Painted]:
        return cls._ipAndPaintedsS.setdefault(ip, [])
    @classmethod
    def paint(cls, ip:str, painted:Painted) -> None:
        with cls._ipAndPaintedsSLock:
            if cls.getRightCountByIp(ip) == 0:
                raise YouDontHaveRights()
            cls._getLogsByIp(ip).append(painted)
    @classmethod
    def getRightCountByIp(cls, ip:str) -> int:
        rights = FIRST_RIGHTS
        previous = None
        def rsA(t):
            nonlocal rights, previous
            rights += int((t - previous) / RIGHT_ACQUIRE_WAIT_SEC)
            if rights > MAX_RIGHTS: rights = MAX_RIGHTS
            elif rights < 0: rights = 0
        with cls._ipAndPaintedsSLock:
            logs = cls._getLogsByIp(ip)
        for i, l in enumerate(logs):
            t = l.timestamp
            rights -= 1
            if i != 0:
                rsA(t)
            previous = t
        if len(logs) != 0: rsA(int(time.time()))
        return rights
    @classmethod
    def getCompactSketch(cls) -> dict[tuple[int, int]:tuple[int, int, int]]:
        with cls._ipAndPaintedsSLock:
            logs = cls._ipAndPaintedsS.copy()
        s = {}
        for ps in logs.values():
            for l in ps:
                s[(l.x, l.y)] = (l.r, l.g, l.b)
        return s
    @classmethod
    def getHistory(cls) -> list[tuple[int,int,int,int,int,int]]:
        with cls._ipAndPaintedsSLock:
            logs = cls._ipAndPaintedsS.copy()
        h = []
        for ps in logs.values():
            for l in ps:
                h.append((l.timestamp, l.x, l.y, l.r, l.g, l.b))
        h = sorted(h, key=lambda l: l[0])
        return h




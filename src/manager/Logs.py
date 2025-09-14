from threading import RLock
import time
from defined import FIRST_RIGHTS, MAX_RIGHTS, RIGHT_ACQUIRE_WAIT_SEC

COLOR = tuple[int, int, int]

class PaintLogTimes:
    _ipAndPaintLogTimeAndColorSS:dict[str:list[tuple[int, COLOR]]] = {}
    _ipAndPaintLogTimeAndColorSSLock = RLock()

    @classmethod
    def _getLogTimesByIp(cls, ip:str) -> list[int]:
        return cls._ipAndPaintLogTimeAndColorSS.setdefault(ip, [])
    @classmethod
    def addIpAndPaintLog(cls, ip:str, logTime:int) -> None:
        with cls._ipAndPaintLogTimeAndColorSSLock:
            cls._getLogTimesByIp(ip).append(logTime)
    @classmethod
    def getRightCountByIp(cls, ip:str) -> int:
        rights = FIRST_RIGHTS
        previous = None
        def rsA(t):
            nonlocal rights, previous
            rights += int((t - previous) / RIGHT_ACQUIRE_WAIT_SEC)
            if rights > MAX_RIGHTS: rights = MAX_RIGHTS
            elif rights < 0: rights = 0
        with cls._ipAndPaintLogTimeAndColorSSLock:
            logs = cls._getLogTimesByIp(ip)
        for i, l in enumerate(logs):
            t = l[0]
            rights -= 1
            if i != 0:
                rsA(t)
            previous = t
        if len(logs) != 0: rsA(int(time.time()))
        return rights
    @classmethod
    def addLog(cls, ip:str,  r:int, g:int, b:int) -> bool:
        with cls._ipAndPaintLogTimeAndColorSSLock:
            if cls.getRightCountByIp(ip) == 0:
                return False
            cls._getLogTimesByIp(ip).append((int(time.time()), (r, g, b)))
        return True 
    
            




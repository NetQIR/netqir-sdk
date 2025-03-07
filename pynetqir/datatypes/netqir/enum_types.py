from enum import Enum

class QCommTypes(Enum):
    TELEDATA = 1
    TELEGATE = 2
    ANY = 3
    
    def __str__(self):
        if self == QCommTypes.TELEDATA:
            return "teledata"
        elif self == QCommTypes.TELEGATE:
            return "telegate"
        elif self == QCommTypes.ANY:
            return ""
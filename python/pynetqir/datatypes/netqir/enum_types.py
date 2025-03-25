from enum import Enum

class QCommTypes(Enum):
    TELEDATA = 1
    TELEGATE = 2
    ANY = 3
    
    def __str__(self):
        if self == QCommTypes.TELEDATA:
            return "_teledata"
        elif self == QCommTypes.TELEGATE:
            return "_telegate"
        elif self == QCommTypes.ANY:
            return ""
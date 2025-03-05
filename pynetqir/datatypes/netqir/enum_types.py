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

class ConditionalType(Enum):
    EQUAL = "eq",
    NOT_EQUAL = "ne",
    GREATER = "gt",
    GREATER_EQUAL = "ge",
    LESS = "lt",
    LESS_EQUAL = "le"

    def __str__(self):
        return self.value[0]
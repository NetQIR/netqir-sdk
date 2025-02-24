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


class Rank:

    total_ranks = 0

    def __init__(self):
        self.value = Rank.total_ranks
        Rank.total_ranks += 1

    def __eq__(self, other):
        if isinstance(other, Rank):
            return self.value == other.value
        return False

    def __repr__(self):
        return f"%r{self.value}"
    
    @staticmethod
    def get_rank(rank):
        r = Rank()
        Rank.total_ranks -= 1
        r.value = rank
        return r 


class ConditionalType(Enum):
    EQUAL = "eq",
    NOT_EQUAL = "ne",
    GREATER = "gt",
    GREATER_EQUAL = "ge",
    LESS = "lt",
    LESS_EQUAL = "le"

    def __str__(self):
        return self.value[0]
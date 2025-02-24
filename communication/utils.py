from enum import Enum


class QCommTypes(Enum):
    TELEDATA = 1
    TELEGATE = 2
    
    def __str__(self):
        return f"{"TELEDATA" if self == QCommTypes.TELEDATA else "TELEGATE"}"


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
        return f"Rank({self.value})"
    
    @staticmethod
    def get_rank(rank):
        r = Rank()
        Rank.total_ranks -= 1
        r.value = rank
        return r 


class ConditionalType(Enum):
    EQUAL = "=",
    NOT_EQUAL = "!=",
    GREATER = ">",
    GREATER_EQUAL = ">=",
    LESS = "<",
    LESS_EQUAL = "<="

    def __str__(self):
        return self.value[0]
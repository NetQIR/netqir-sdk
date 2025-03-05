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
        return f"%rk{self.value}"
    
    @staticmethod
    def get_rank(rank):
        r = Rank()
        Rank.total_ranks -= 1
        r.value = rank
        return r 
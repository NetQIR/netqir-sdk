from python.pynetqir.datatypes import Register


class Result(Register):
    total_results = 0

    def __init__(self):
        super().__init__()
        self.identifier = Result.total_results
        Result.total_results += 1

    def __repr__(self):
        return f"%r{self.identifier}"

    @staticmethod
    def datatype_default() -> str:
        return f"%{__class__.__name__}*"


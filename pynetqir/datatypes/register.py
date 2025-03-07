class Register():

    total = 0

    def __init__(self):
        self.identifier = Register.total
        Register.total += 1

    def __repr__(self):
        return f"%rg{self.identifier}"

    def datatype(self) -> str:
        return f"%{self.__class__.__name__}*"

class TemporalRegister(Register):
    total_temporal_registers = 0

    def __init__(self, name=""):
        super().__init__()
        self.identifier = TemporalRegister.total_temporal_registers
        TemporalRegister.total_temporal_registers += 1
        self.name = name

    def __repr__(self):
        return f"%t{self.identifier}{self.name}"

    def __str__(self):
        return self.__repr__()
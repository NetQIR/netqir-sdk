class Register:

    total = 0

    def __init__(self):
        self.identifier = Register.total
        Register.total += 1

    def __repr__(self):
        return f"%rg{self.identifier}"

    def datatype(self) -> str:
        return f"%{self.__class__.__name__}*"

    @staticmethod
    def datatype_default() -> str:
        return f"%{__class__.__name__}*"

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

class InmediateRegister(Register):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def datatype(self) -> str:
        return f"i32"

class NamedRegister(Register):
    def __init__(self, name, datatype = "i32"):
        super().__init__()
        self.name = name
        self.__datatype = datatype

    def __repr__(self):
        return f"%{self.name}"

    def datatype(self) -> str:
        return f"{self.__datatype}"
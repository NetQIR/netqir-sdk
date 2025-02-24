class TemporalRegister:
    total_temporal_registers = 0

    def __init__(self, name=""):
        self.identifier = TemporalRegister.total_temporal_registers
        TemporalRegister.total_temporal_registers += 1
        self.name = name

    def __repr__(self):
        return f"%t{self.identifier}{self.name}"
    
    def __str__(self):
        return self.__repr__()
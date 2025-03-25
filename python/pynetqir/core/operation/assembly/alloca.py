from python.pynetqir.core.operation import Operation
from python.pynetqir.datatypes import Register
from typing import Callable


class AllocateOperation(Operation):

    @staticmethod
    def allocate_register(num_register : int, constructor: Callable[[], Register]):
        registers = [constructor() for _ in range(num_register)]
        allocations = [AllocateOperation(r) for r in registers]

        return registers, allocations

    def __init__(self, register : Register):
        super().__init__()
        self.register = register
        self.datatype = register.datatype()

    def __str__(self):
        return f"{self.register} = alloca {self.register.datatype()}"
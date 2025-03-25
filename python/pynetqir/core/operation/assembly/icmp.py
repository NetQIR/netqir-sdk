from python.pynetqir.core.operation import Operation
from python.pynetqir.datatypes import Register


class ICMPOperation(Operation):
    def __init__(self, comparision: str, left: str, right: str, return_register : Register):
        super().__init__()
        self.comparision = comparision
        self.left = left
        self.right = right
        self.return_register = return_register

    def __str__(self):
        return f"{self.return_register} = icmp {self.comparision} i32 {self.left}, {self.right}"
from typing import List
from python.pynetqir.core.operation import Operation
from python.pynetqir.datatypes import Register


class Parameter:
    def __init__(self, name : str = "", type : str = "", register : Register = None):
        self.name = name
        self.type = type
        self.register = register

        if register is not None:
            self.name = register.__repr__()
            self.type = register.datatype()

    def __str__(self):
        return f"{self.type} {self.name}"

class Function(Operation):
    def __init__(self, name, return_type="void", parameters: List[Parameter] = [], return_register: Register = None):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.return_register = return_register

    def print_without_parameter_name(self):
        return f"{self.return_type} @{self.name}({', '.join([p.type for p in self.parameters])})"

    def __str__(self):
        return_type = self.return_type
        if return_type is None:
            return_type = "void"
        return f"{return_type} @{self.name}({', '.join([str(p) for p in self.parameters])})"

    def __eq__(self, other):
        """
        Check if two functions are equal by comparing their name, return type, and parameter
        types. The order of the parameters matters.
        """

        if not isinstance(other, Function):
            return False
        # Check if the name, return type, and parameter types are equal
        return (self.name == other.name and
                self.return_type == other.return_type and
                all(p1.type == p2.type for p1, p2 in zip(self.parameters, other.parameters)))

    def __hash__(self):
        return hash((self.name, self.return_type, tuple(p.type for p in self.parameters)))

class DeclarationFunction(Operation):
    def __init__(self, function: Function):
        self.function = function
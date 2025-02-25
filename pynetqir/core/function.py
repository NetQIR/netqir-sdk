from typing import List

class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.type} {self.name}"
    
class Function:
    def __init__(self, name, return_type, parameters : List[Parameter]):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters

    def __str__(self):
        return_type = self.return_type
        if return_type == None:
            return_type = "void"
        return f"{return_type} @{self.name}({', '.join([str(p) for p in self.parameters])})"
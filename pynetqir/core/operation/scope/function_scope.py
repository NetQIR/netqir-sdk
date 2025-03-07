from pynetqir.core.operation import Function
from pynetqir.core.operation.scope import Scope

class FunctionScope(Scope):

    def __init__(self, function : Function):
        super().__init__()
        self.__function = function
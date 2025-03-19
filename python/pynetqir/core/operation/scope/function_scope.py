from python.pynetqir.core.operation import Function
from python.pynetqir.core.operation.scope import Scope

class FunctionScope(Scope):

    def __init__(self, parent: Scope, function : Function):
        super().__init__(parent)
        self.function = function
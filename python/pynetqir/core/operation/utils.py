from python.pynetqir.core.operation import Operation


class BarrierOperation(Operation):
    def __init__(self):
        super().__init__()

class DatatypeDeclarationOperation(Operation):
    def __init__(self, datatype: str, creation: str = "type opaque"):
        super().__init__()
        self.datatype = datatype
        self.creation = creation
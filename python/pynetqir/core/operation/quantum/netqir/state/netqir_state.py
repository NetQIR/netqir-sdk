from python.pynetqir.core.operation.quantum.netqir import NetQIROperation


class Initialize(NetQIROperation):
    def __init__(self):
        super().__init__("initialize")

class Finalize(NetQIROperation):
    def __init__(self):
        super().__init__("finalize")
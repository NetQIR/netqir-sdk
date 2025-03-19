from python.pynetqir.datatypes import Register

class CommunicatorRegister(Register):
    total_communicators  = 0

    def __init__(self):
        super().__init__()
        self.identifier = CommunicatorRegister.total_communicators
        CommunicatorRegister.total_communicators += 1

    @staticmethod
    def get_comm_world():
        return NamedCommunicatorRegister("netqir_comm_world")

    def __repr__(self):
        return f"%cm{self.identifier}"

    def datatype(self) -> str:
        return f"%Comm*"

class NamedCommunicatorRegister(CommunicatorRegister):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"@{self.name}"
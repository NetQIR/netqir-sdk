from python.pynetqir.core.operation import Parameter
from python.pynetqir.core.operation.quantum.netqir import NetQIROperation
from python.pynetqir.datatypes import Register
from python.pynetqir.datatypes.netqir import Rank
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister

class GetRankOperation(NetQIROperation):
    def __init__(self, comm : CommunicatorRegister, rank : Rank):
        super().__init__("comm_rank", parameters=[Parameter(register=comm), Parameter(register=rank)])
        self.comm = comm
        self.rank = rank

class GetCommSizeOperation(NetQIROperation):
    def __init__(self, comm : CommunicatorRegister, register : Register):
        super().__init__("comm_size", parameters=[Parameter(register=comm), Parameter(register=register)])
        self.comm = comm
from typing import List, Tuple

from python.pynetqir.core.operation import Operation
from python.pynetqir.core.operation.assembly import AllocateOperation
from python.pynetqir.core.operation.quantum.netqir.communication.p2p import QuantumP2POperation
from python.pynetqir.core.operation.quantum.netqir.operate_datatype import GetRankOperation, GetCommSizeOperation
from python.pynetqir.datatypes import Register
from python.pynetqir.datatypes.netqir import Rank
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister
from python.pynetqir.datatypes.qir import Qubit

class NetQIROperations:

    @staticmethod
    def get_rank(comm: CommunicatorRegister) -> Tuple[Rank, List[Operation]]:
        rank = Rank()
        allocate_op = AllocateOperation(rank)
        get_rank_op = GetRankOperation(comm, rank)

        return rank, [allocate_op, get_rank_op]

    @staticmethod
    def get_comm_size(comm: CommunicatorRegister, register: Register) -> GetCommSizeOperation:
        return GetCommSizeOperation(comm, register)

    @staticmethod
    def qsend(comm: CommunicatorRegister, qubit: Qubit, rank: Rank) -> QuantumP2POperation:
        return QuantumP2POperation("qsend", comm, qubit, rank)

    @staticmethod
    def qrecv(comm: CommunicatorRegister, qubit: Qubit, rank: Rank) -> QuantumP2POperation:
        return QuantumP2POperation("qrecv", comm, qubit, rank)
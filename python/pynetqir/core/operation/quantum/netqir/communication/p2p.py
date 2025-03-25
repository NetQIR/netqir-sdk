from python.pynetqir.core.operation import Parameter
from python.pynetqir.core.operation.quantum.netqir import NetQIROperation
from python.pynetqir.datatypes.netqir import Rank, QCommTypes
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister
from python.pynetqir.datatypes.qir import Qubit

class QuantumP2POperation(NetQIROperation):
    def __init__(self, name : str, comm: CommunicatorRegister, qubit: Qubit, rank: Rank,
                 comm_type: QCommTypes = QCommTypes.ANY):

        super().__init__(f"{name}{comm_type}", parameters=[Parameter(register=qubit), Parameter(register=rank), Parameter(register=comm)])
        self.comm = comm
        self.qubit = qubit
        self.rank = rank

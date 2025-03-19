from python.pynetqir.core import Program
from python.pynetqir.core.operation import Function, ConditionalOperator
from python.pynetqir.core.operation.assembly import AllocateOperation
from python.pynetqir.core.operation.conditional import ConditionalType
from python.pynetqir.core.operation.quantum.gates.gates import QuantumGates
from python.pynetqir.core.operation.quantum.netqir import NetQIROperations
from python.pynetqir.core.operation.scope import FunctionScope
from python.pynetqir.datatypes.netqir import Rank
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister
from python.pynetqir.datatypes.netqir.rank import InmediateRank
from python.pynetqir.datatypes.qir import Qubit, Result

# Create a Program
program = Program()
program.start()

gscope = Program.get_instance().get_global_scope()

# Create a FunctionScope
main = FunctionScope(gscope, Function("main"))

qreg, allocate_qreg = AllocateOperation.allocate_register(2, Qubit)
creg, allocate_creg = AllocateOperation.allocate_register(1, Result)
my_rank = Rank()
comm_world = CommunicatorRegister.get_comm_world()

main.add_operations(allocate_qreg)
main.add_operations(allocate_creg)

scope1 = main.give_birth()

scope1.add_operation(QuantumGates.H(qreg[0]))
scope1.add_operation(QuantumGates.CNOT(qreg[0], qreg[1]))

main.add_operation(QuantumGates.mz(qreg[0], creg[0]))

main.add_operation(QuantumGates.classical_controlled(creg[0], QuantumGates.X(qreg[1])))

my_rank, operations = NetQIROperations.get_rank(comm_world)
main.add_operations(operations)
main.add_operation(NetQIROperations.get_comm_size(comm_world, my_rank))
main.add_operation(ConditionalOperator(ConditionalType.EQUAL, my_rank, InmediateRank(0),
                                       [NetQIROperations.qsend(comm_world, qreg[0], InmediateRank(1))],
                                       [NetQIROperations.qrecv(comm_world, qreg[1], InmediateRank(0))]))

program.run()

program.end()

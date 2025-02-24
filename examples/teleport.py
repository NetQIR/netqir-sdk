from PyNetQIR.core import Environment
from PyNetQIR.quantum.gates import QuantumGate
from PyNetQIR.communication.communicator import Communicator
from PyNetQIR.communication.utils import QCommTypes, Rank, ConditionalType

# Initialize the quantum environment with a name and the number of qubits and classical bits
env = Environment("teleport", 2, 1)

# Initialize the communicator with the number of processes or nodes
comm = Communicator(2)

# Get the quantum and classical registers
qreg = env.get_qubits()
creg = env.get_results()

# Get the rank of the current process and the total number of processes
my_rank = comm.get_rank()
size = comm.get_size_world()

# Apply a Hadamard gate to the first qubit
QuantumGate.H(qreg[0])
# Apply a CNOT gate with the first qubit as control and the second as target
QuantumGate.CNOT(qreg[0], qreg[1])

# Insert a barrier
QuantumGate.barrier()

# Measure the first qubit and store the result in the first classical bit
QuantumGate.mz(qreg[0], creg[0])

# Apply an X gate to the second qubit if the measurement result is 1, otherwise apply the identity gate
QuantumGate.if_result(creg[0], qreg[1], QuantumGate.X, QuantumGate.I)

# Conditional communication based on the rank of the process
comm.conditional_by_rank(ConditionalType.GREATER_EQUAL, my_rank, "0",
                         lambda: comm.qsend("1", qreg[0], QCommTypes.TELEDATA),
                         lambda: comm.qrecv("0", qreg[0], QCommTypes.TELEDATA))

# Finalize the quantum environment
env.finalize()

# NetQIR SDK
NetQIR SDK is a set of tools for developing NetQIR codes through various high-level languages such as Python (PyNetQIR) or Rust (RustNetQIR).

## PyNetQIR

### Examples
The examples can be found in the `python/examples` directory.

#### Quantum Teleportation
```python
from python.pynetqir.core import Program
from python.pynetqir.core.builders.scope_builder import MainScopeBuilder, FunctionScopeBuilder
from python.pynetqir.core.operation import Function, Parameter
from python.pynetqir.core.operation.conditional import ConditionalType
from python.pynetqir.datatypes.netqir.rank import InmediateRank
from python.pynetqir.datatypes.qir import Qubit

# Create a Program
program = Program()
program.start()

# Get the global scope of the program
gscope = Program.get_instance().get_global_scope()

"""
 - Define a new function for generate an entanglement between two qubits
"""
# Function signature
entgl_func = Function("entanglement", "void", [Parameter(register=Qubit()), Parameter(register=Qubit())])
entgl_builder = FunctionScopeBuilder(2, 0, entgl_func)  # Builder for the function scope
entgl_builder.h(0).cx(0, 1)  # Add operations to the function scope
entgl_builder.build(gscope)  # Build the function scope

"""
 - Main scope
"""
main_scope = MainScopeBuilder(4, 2)  # Create the main scope builder
main_scope.call(entgl_func, 1, 2)  # Call the entanglement function
main_scope.mz(0, 0)
main_scope.mz(1, 1)
main_scope.classical_controlled(0, lambda: main_scope.x(3))
main_scope.classical_controlled(1, lambda: main_scope.x(3))
main = main_scope.build(gscope)  # Build the main scope linked to the global scope
program.run() # Run program
```

#### Quantum send and receive using NetQIR
```python
from python.pynetqir.core import Program
from python.pynetqir.core.builders.scope_builder import MainScopeBuilder
from python.pynetqir.core.operation.conditional import ConditionalType
from python.pynetqir.datatypes.netqir.rank import InmediateRank

program = Program()

program.start()  # start the program
gscope = program.get_global_scope()  # get the global scope
comm_world = program.get_comm_world()  # get the communicator world

main = MainScopeBuilder(1, 0) # Create a builder for the main scope
main.netqir_initialize() # Initialize the NetQIR environment

# Get my rank and the size of the communicator
my_rank = main.get_rank(comm_world)
main.get_comm_size(comm_world, program.get_size_world_register())

# Create a conditional operator
#
# if my_rank == 0:
#   main.qsend(comm_world, 0, 1)
# else:
#   main.qrecv(comm_world, 0, 0)
main.conditional(ConditionalType.EQUAL, my_rank, InmediateRank(0),
                 [lambda: main.qsend(comm_world, 0, 1)],
                 [lambda: main.qrecv(comm_world, 0, 0)])

main.netqir_finalize() # Finalize the NetQIR environment

main.build(gscope) # Important! Build the main scope linked to the global scope

program.run() # Run the program
program.end() # End the program
```
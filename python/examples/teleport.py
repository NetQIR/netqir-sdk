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

main = main_scope.build(gscope)  # Build the main scope

# Run program
program.run()
program.end()
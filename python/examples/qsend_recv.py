from python.pynetqir.core import Program
from python.pynetqir.core.builders.scope_builder import MainScopeBuilder
from python.pynetqir.core.operation.conditional import ConditionalType
from python.pynetqir.datatypes.netqir.rank import InmediateRank

program = Program()

program.start()  # start the program
gscope = program.get_global_scope()  # get the global scope
comm_world = program.get_comm_world()  # get the communicator world

# Create a builder for the main scope
main = MainScopeBuilder(1, 0)

# Initialize the NetQIR environment
main.netqir_initialize()

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

# Finalize the NetQIR environment
main.netqir_finalize()

# Important! Build the main scope linked to the global scope
main.build(gscope)

# Run the program
program.run()

# End the program
program.end()
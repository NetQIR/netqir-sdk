from enum import Enum
from PyNetQIR.communication.utils import Rank, QCommTypes, ConditionalType
from PyNetQIR.quantum import Qubit
from PyNetQIR.core import Printer
from typing import Callable


class Communicator:

    def __init__(self, num_nodes):
        self.num_nodes = num_nodes

    def get_rank(self):
        r = Rank()
        Printer.get_printer().print_get_rank(r)
        return r
    
    def get_size_world(self):
        Printer.get_printer().print_get_size_world()
        return self.num_nodes

    def qsend(self, rank_dest: Rank, qubit: Qubit, comm_type: QCommTypes):
        Printer.get_printer().print_point_to_point_comm(
            "qsend", qubit, rank_dest, comm_type)

    def qrecv(self, rank_src, qubit, comm_type: QCommTypes):
        Printer.get_printer().print_point_to_point_comm(
            "qrecv", qubit, rank_src, comm_type)

    def conditional_by_rank(self, comp_type: ConditionalType,
                            rank_left: Rank, rank_right: Rank,
                            lambda_true: Callable[[], None],
                            lambda_false: Callable[[], None]):
        Printer.get_printer().print_conditional(comp_type, rank_left,
                                                rank_right, lambda_true, 
                                                lambda_false)

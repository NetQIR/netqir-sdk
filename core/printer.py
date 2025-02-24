from PyNetQIR.quantum import Qubit
from PyNetQIR.classical import Result
from PyNetQIR.communication.utils import Rank, QCommTypes, ConditionalType
from typing import Callable

import sys


class Printer:
    _instance = None

    def __new__(cls, filename):
        if cls._instance is None:
            cls._instance = super(Printer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename):
        if self._initialized:
            return
        # self.file = open(filename, "w")
        self.file = sys.stdout
        self._initialized = True

    @staticmethod
    def get_printer():
        return Printer._instance

    def print_single_gate(self, gate: str, qubit: Qubit):
        self.file.write(f"{gate} {qubit}\n")

    def print_two_qubit_gate(self, gate, qubit1: Qubit, qubit2: Qubit):
        self.file.write(f"{gate} {qubit1} {qubit2}\n")

    def print_measurement(self, qubit: Qubit, result: Result):
        self.file.write(f"MEASURE {qubit} -> {result}\n")

    def print_three_qubit_gate(self, gate, qubit1: Qubit, qubit2: Qubit, qubit3: Qubit):
        self.file.write(f"{gate} {qubit1} {qubit2} {qubit3}\n")

    def print_conditional_gate(self, gate_one, gate_zero, qubit: Qubit, result: Result):
        self.file.write(
            f"IF {qubit} == {result}\nTHEN\n\t")
        gate_one(qubit)
        self.file.write("ELSE\n\t")
        gate_zero(qubit)
        self.file.write("FI\n")

    def print_barrier(self):
        self.file.write("BARRIER\n")

    def print_param_gate(self, gate, param, qubit: Qubit):
        self.file.write(f"{gate} {param} {qubit}\n")

    def print_blank_line(self):
        self.file.write("\n")

    def print_conditional(self, comp_type: ConditionalType, rank_left: Rank,
                          rank_right: Rank, lambda_true: Callable[[], None],
                          lambda_false: Callable[[], None]):
        self.file.write(f"IF {rank_left} {comp_type} {rank_right}\nTHEN\n\t")
        lambda_true()
        self.file.write("ELSE\n\t")
        lambda_false()
        self.file.write("FI\n")

    def print_get_rank(self, rank):
        self.file.write(f"{rank} = GET_RANK\n")

    def print_get_size_world(self):
        self.file.write("%size_world = GET_SIZE_WORLD\n")

    def print_point_to_point_comm(self, operation: str, qubit: Qubit,
                                  rank: Rank, comm_type: QCommTypes):
        self.file.write(f"{operation}_{comm_type} {qubit} {rank}\n")

    def close(self):
        self.file.close()
        self._initialized = False
        Printer._instance = None

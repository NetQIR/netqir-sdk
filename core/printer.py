from PyNetQIR.quantum import Qubit
from PyNetQIR.classical import Result, TemporalRegister
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
        self.pre_print = ""
        self._initialized = True
        self.funtions_to_declare = []

    @staticmethod
    def get_printer():
        return Printer._instance

    @staticmethod
    def __qubit_datatype():
        return f"%{Qubit.__name__}*"

    @staticmethod
    def __result_datatype():
        return f"%{Result.__name__}*"
    
    @staticmethod
    def __comm_datatype():
        return f"%Comm*"

    def __print(self, str):
        self.file.write(f"{self.pre_print}{str}")

    def __print_call(self, str, return_type="void", return_register=""):
        pre = ""
        if return_register:
            pre = f"{return_register} = "
        self.__print(f"{pre}call {return_type} @{str}\n")

    def print_initialize(self):
        self.__print("%Qubit = type opaque\n"
                     "%Result = type opaque\n"
                     "%Comm = type opaque\n"

                     "define void @main(i32 noundef %0, ptr noundef %1) #0 {\n"
                     "\tentry:\n")
        self.pre_print = "\t\t"

    def print_alloca(self, register, datatype):
        self.__print(f"{register} = alloca %{datatype}\n")

    def print_single_gate(self, gate: str, qubit: Qubit):
        self.__print_call(
            f"__quantum__qis__{gate.lower()}__body({Printer.__qubit_datatype()} {qubit})"
        )

    def print_two_qubit_gate(self, gate: str, qubit1: Qubit, qubit2: Qubit):
        self.__print_call(
            f"__quantum__qis__{gate.lower()}__body({Printer.__qubit_datatype()} {qubit1}, {Printer.__qubit_datatype()} {qubit2})\n"
        )

    def print_measurement(self, qubit: Qubit, result: Result):
        self.__print(
            f"@__quantum__qis__mz__body({Printer.__qubit_datatype()} {qubit}, {Printer.__result_datatype()} {result})\n")

    def print_three_qubit_gate(self, gate: str, qubit1: Qubit, qubit2: Qubit, qubit3: Qubit):
        self.__print_call(
            f"__quantum__qis__{gate.lower()}__body({Printer.__qubit_datatype()} {qubit1}, {Printer.__qubit_datatype()} {qubit2}, {Printer.__qubit_datatype()} {qubit3}\n")

    def print_conditional_gate(self, gate_one, gate_zero, qubit: Qubit, result: Result):
        self.print_conditional(ConditionalType.EQUAL, qubit, result, lambda: gate_one(qubit), lambda: gate_zero(qubit))

    def print_barrier(self):
        self.__print_call("__quantum__qis__barrier__body()")

    def print_param_gate(self, gate, param, qubit: Qubit):
        self.__print(f"{gate} {param} {qubit}\n")

    def print_blank_line(self):
        self.__print("\n")

    def print_conditional(self, comp_type: ConditionalType, rank_left: Rank,
                          rank_right: Rank, lambda_true: Callable[[], None],
                          lambda_false: Callable[[], None]):
        tmp = TemporalRegister()
        tmp_true = TemporalRegister("_true")
        tmp_false = TemporalRegister("_false")
        tmp_join = TemporalRegister("_continue")
        
        # icmp instruction
        self.__print(f"{tmp} = icmp {comp_type} i32 {rank_left}, {rank_right}\n")
        
        # branch instruction
        self.__print(f"br i1 {tmp}, label {tmp_true}, label {tmp_false}\n")

        # return \t for the next instructions
        self.pre_print = self.pre_print[:-1]
        self.__print(f"{tmp_true}:\n")
        self.pre_print += "\t"
        lambda_true()
        self.__print(f"br label {tmp_join}\n")
        self.pre_print = self.pre_print[:-1]
        self.__print(f"{tmp_false}:\n")
        self.pre_print += "\t"
        lambda_false()
        self.__print(f"br label {tmp_join}\n")
        self.pre_print = self.pre_print[:-1]

        self.__print(f"{tmp_join}:\n")
        self.pre_print += "\t"

    def print_get_rank(self, rank):
        self.__print_call(f"__netqir__comm_rank({Printer.__comm_datatype()} @netqir_comm_world, ptr {rank})", "i32")

    def print_get_size_world(self):
        self.__print_call(f"__netqir__comm_size({Printer.__comm_datatype()} @netqir_comm_world)", "i32", "%size_world")

    def print_point_to_point_comm(self, operation: str, qubit: Qubit,
                                  rank: Rank, comm_type: QCommTypes):
        separation = '_' if comm_type != QCommTypes.ANY else ''
        self.__print_call(
            f"__netqir__{operation}{separation}{comm_type}({Printer.__qubit_datatype()} {qubit}, i32 {rank})", "i32")

    def close_function(self):
        self.__print_call("__netqir__finalize()")
        self.pre_print = ""
        self.__print("}\n")

    def close(self):
        self.file.close()
        self._initialized = False
        Printer._instance = None

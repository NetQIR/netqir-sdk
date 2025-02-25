from pynetqir.quantum import Qubit
from pynetqir.classical import Result, TemporalRegister
from pynetqir.communication.utils import Rank, QCommTypes, ConditionalType
from pynetqir.core.function import Function, Parameter
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
        self.funtions_to_declare = set()

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

    @staticmethod
    def __register_size_world():
        return "%size_world"

    def __print(self, str):
        self.file.write(f"{self.pre_print}{str}")

    def __print_call(self, function: Function, return_register=""):
        # Append call to the set of functions to declare
        self.funtions_to_declare.add(function)

        pre = ""
        if return_register:
            pre = f"{return_register} = "
        self.__print(f"{pre}call {function};\n")

    def print_initialize(self):
        self.__print("%Qubit = type opaque\n"
                     "%Result = type opaque\n"
                     "%Comm = type opaque\n"
                     f"{Printer.__register_size_world()} = alloca i32\n\n"

                     "define void @main(i32 noundef %0, ptr noundef %1) #0 {\n"
                     "\tentry:\n")
        self.pre_print = "\t\t"

        initialize = Function("__netqir__initialize", "void", [])

        self.__print_call(initialize)
        self.print_blank_line()

    def print_alloca(self, register, datatype):
        self.__print(f"{register} = alloca %{datatype};\n")

    def print_single_gate(self, gate: str, qubit: Qubit):

        single_gate = Function(f"__quantum__qis__{gate.lower()}__body", "void",
                               [Parameter(qubit, Printer.__qubit_datatype())]
                               )

        self.__print_call(single_gate)

    def print_two_qubit_gate(self, gate: str, qubit1: Qubit, qubit2: Qubit):

        two_qubit_gate = Function(f"__quantum__qis__{gate.lower()}__body", "void",
                                  [Parameter(qubit1, Printer.__qubit_datatype()),
                                   Parameter(qubit2, Printer.__qubit_datatype())]
                                  )

        self.__print_call(two_qubit_gate)

    def print_measurement(self, qubit: Qubit, result: Result):
        measurement = Function("__quantum__qis__mz__body", "void",
                               [Parameter(qubit, Printer.__qubit_datatype()),
                                Parameter(result, Printer.__result_datatype())]
                               )
        self.__print_call(measurement)

    def print_three_qubit_gate(self, gate: str, qubit1: Qubit, qubit2: Qubit, qubit3: Qubit):

        qubit_gate = Function(f"__quantum__qis__{gate.lower()}__body", "void",
                              [Parameter(qubit1, Printer.__qubit_datatype()),
                               Parameter(qubit2, Printer.__qubit_datatype()),
                               Parameter(qubit3, Printer.__qubit_datatype())]
                              )

        self.__print_call(qubit_gate)

    def print_conditional_gate(self, gate_one, gate_zero, qubit: Qubit, result: Result):
        self.print_conditional(ConditionalType.EQUAL, qubit, result, lambda: gate_one(
            qubit), lambda: gate_zero(qubit))

    def print_barrier(self):
        barrier = Function("__quantum__qis__barrier__body", "void", [])
        self.__print_call(barrier)

    def print_param_gate(self, gate, param, qubit: Qubit):
        param_gate = Function(f"__quantum__qis__{gate.lower()}__body", "void",
                              [Parameter(qubit, Printer.__qubit_datatype()),
                               Parameter(param, "i32")]
                              )

        self.__print_call(param_gate)

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
        self.__print(
            f"{tmp} = icmp {comp_type} i32 {rank_left}, {rank_right};\n")

        # branch instruction
        self.__print(f"br i1 {tmp}, label {tmp_true}, label {tmp_false};\n")

        # return \t for the next instructions
        self.pre_print = self.pre_print[:-1]
        self.__print(f"{tmp_true}:\n")
        self.pre_print += "\t"
        lambda_true()
        self.__print(f"br label {tmp_join};\n")
        self.pre_print = self.pre_print[:-1]
        self.__print(f"{tmp_false}:\n")
        self.pre_print += "\t"
        lambda_false()
        self.__print(f"br label {tmp_join};\n")
        self.pre_print = self.pre_print[:-1]

        self.__print(f"{tmp_join}:\n")
        self.pre_print += "\t"

    def print_get_rank(self, rank):
        comm_rank = Function("__netqir__comm_rank", "i32",
                             [Parameter("@netqir_comm_world",
                                        Printer.__comm_datatype()),

                              Parameter(rank, "ptr")
                              ]
                             )
        self.__print_call(comm_rank)

    def print_get_size_world(self):
        comm_size_world = Function("__netqir__comm_size", "i32",
                                   [Parameter("@netqir_comm_world",
                                              Printer.__comm_datatype()),

                                       Parameter(
                                           Printer.__register_size_world(), "ptr")
                                    ]
                                   )
        self.__print_call(comm_size_world)

    def print_point_to_point_comm(self, operation: str, qubit: Qubit,
                                  rank: Rank, comm_type: QCommTypes):
        separation = '_' if comm_type != QCommTypes.ANY else ''

        point_to_point = Function(f"__netqir__{operation}{separation}{comm_type}", "i32",
                                  [Parameter(qubit, Printer.__qubit_datatype()),
                                   Parameter(rank, "i32")]
                                  )

        self.__print_call(point_to_point)

    def close_function(self):
        finalize = Function("__netqir__finalize", "void", [])
        self.__print_call(finalize)
        self.pre_print = ""
        self.__print("}\n")

    def declarate_functions(self):
        # Order functions by name
        self.funtions_to_declare = sorted(
            self.funtions_to_declare, key=lambda x: x.name)

        for function in self.funtions_to_declare:
            self.__print(f"declare {function.print_without_parameter_name()};\n")

    def close(self):
        self.file.close()
        self._initialized = False
        Printer._instance = None

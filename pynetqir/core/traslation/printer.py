from pynetqir.core.operation import Operation, ConditionalOperator
from pynetqir.core.operation.conditional import ConditionalType
from pynetqir.core.operation.quantum.gates import *
from pynetqir.core.traslation import Executor
from pynetqir.datatypes import TemporalRegister
from pynetqir.datatypes.qir import Qubit, Result
from pynetqir.datatypes.netqir import Rank, QCommTypes
from pynetqir.core.operation.function import Function, Parameter
from typing import Callable

import sys


class PrinterExecutor(Executor):

    def __init__(self, stream=sys.stdout):
        self.__init__()
        self.__stream = stream
        self.__indentations = 0

    def print(self, message, endline = "\n"):
        self.__stream.write("\t" * self.__indentations)
        self.__stream.write(message)
        self.__stream.write(endline)

    def __remove_indentation(self):
        self.__indentations -= 1 if self.__indentations > 0 else 0

    def run_single_qubit_gate(self, operator: SingleGateOperation):
        self.run_qir_gate(operator)

    def run_multiple_qubit_gate(self, operator: MultipleGateOperation):
        self.run_qir_gate(operator)

    def run_controlled_qubit_gate(self, operator: ControlledGateOperation):
        self.run_qir_gate(operator)

    def run_parameterized_qubit_gate(self, operator: ParameterizedGateOperation):
        self.run_qir_gate(operator)

    def run_measurement_gate(self, operator: MeasurementGateOperation):
        self.run_qir_gate(operator)

    def run_reset_gate(self, operator: ResetGateOperation):
        self.run_qir_gate(operator)

    def run_conditional_operator(self, operator: ConditionalOperator):
        tmp = TemporalRegister()
        tmp_true = TemporalRegister("_true")
        tmp_false = TemporalRegister("_false")
        tmp_join = TemporalRegister("_join")

        # ICMP instruction
        self.print(f"{tmp} = icmp {operator.comm_type} i32 {operator.left}, {operator.right}")

        # BRANCH instruction
        self.print(f"br i1 {tmp}, label {tmp_true}, label {tmp_false}")

        # Remove Indentation
        self.__remove_indentation()

        # True branch
        self.print(f"{tmp_true}:")
        self.__indentations += 1
        [self.run(op) for op in operator.operators_true]
        self.print(f"br label {tmp_join}")

        # Remove indentation
        self.__remove_indentation()

        # False branch
        self.print(f"{tmp_false}:\n")
        self.__indentations += 1
        [self.run(op) for op in operator.operators_false]
        self.print(f"br label {tmp_join}")
        self.print(f"br label {tmp_false}")

        # Remove indentation
        self.__remove_indentation()

        # Join
        self.print(f"{tmp_join}:\n")
        self.__indentations += 1

    def run_qir_gate(self, operator: GateOperation):
        self.run_function(operator, prename="__quantum__qis__", postname="__body")

    def run_function(self, operator: Function, prename = "", postname = ""):
        msg = f"{prename}{operator.name}{postname}("
        for i, parameter in enumerate(operator.parameters):
            if i > 0:
                msg += ", "
            msg += f"{parameter.type} {parameter.name}"

        self.print(msg)

    def run(self, operator: Operation):
        super().run(operator)

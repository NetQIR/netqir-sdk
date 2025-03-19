from python.pynetqir.core.operation import Operation, ConditionalOperator
from python.pynetqir.core.operation.assembly import AllocateOperation, ICMPOperation, UnconditionalBranchOperation, \
    ConditionalBranchOperation
from python.pynetqir.core.operation.scope import FunctionScope, Scope
from python.pynetqir.core.operation.utils import DatatypeDeclarationOperation
from python.pynetqir.core.traslation import Executor
from python.pynetqir.datatypes import TemporalRegister
from python.pynetqir.core.operation.function import Function, DeclarationFunction

import sys


class PrinterExecutor(Executor):

    def __init__(self, stream=sys.stdout):
        super().__init__()
        self.__stream = stream
        self.__indentations = 0

    def print(self, message, endline = "\n"):
        self.__stream.write("\t" * self.__indentations)
        self.__stream.write(message)
        self.__stream.write(endline)

    def __remove_indentation(self):
        self.__indentations -= 1 if self.__indentations > 0 else 0

    def __increment_indentation(self):
        self.__indentations += 1

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

    def run_conditional_branch_operation(self, operator: ConditionalBranchOperation):
        pass

    def run_unconditional_branch_operation(self, operator: UnconditionalBranchOperation):
        pass

    def run_icmp_operation(self, operator: ICMPOperation):
        pass

    def run_allocate_operation(self, operator: AllocateOperation):
        self.print(f"{operator.register} = alloca {operator.datatype};")

    def run_classical_controlled_gate(self, operator: ClassicalControlledGateOperation):
        self.run_conditional_operator(operator.conditional_operation)

    def run_conditional_operator(self, operator: ConditionalOperator):
        tmp = TemporalRegister()
        tmp_true = TemporalRegister("_true")
        tmp_false = TemporalRegister("_false")
        tmp_join = TemporalRegister("_join")

        # ICMP instruction
        self.print(f"{tmp} = icmp {operator.comm_type} i32 {operator.left}, {operator.right};")

        # BRANCH instruction
        self.print(f"br i1 {tmp}, label {tmp_true}, label {tmp_false};")

        # Remove Indentation
        self.__remove_indentation()

        # True branch
        self.print(f"{tmp_true}:")
        self.__increment_indentation()

        [self.run(op) for op in operator.operators_true]
        self.print(f"br label {tmp_join};")

        # Remove indentation
        self.__remove_indentation()

        # False branch
        self.print(f"{tmp_false}:")
        self.__increment_indentation()
        [self.run(op) for op in operator.operators_false]
        self.print(f"br label {tmp_join};")

        # Remove indentation
        self.__remove_indentation()

        # Join
        self.print(f"{tmp_join}:\n")
        self.__increment_indentation()

    def run_qir_gate(self, operator: GateOperation):
        self.run_function(operator, prename="__quantum__qis__", postname="__body")

    @staticmethod
    def __function_name(operator: Function, prename = "", postname = "", with_register = True):
        msg = f"{operator.return_type} @{prename}{operator.name.lower()}{postname}("
        for i, parameter in enumerate(operator.parameters):
            if i > 0:
                msg += ", "
            msg += f"{parameter.type}{' ' + str(parameter.name) if with_register else ''}"

        msg += ")"

        return msg

    def run_function(self, operator: Function, prename = "", postname = ""):
        name = PrinterExecutor.__function_name(operator, prename, postname)

        if operator.return_register is not None:
            self.print(f"{operator.return_register} = call {name};")
        else:
            self.print(f"call {name};")

    def run_function_scope(self, operator: FunctionScope):
        name = PrinterExecutor.__function_name(operator.function)

        self.print(f"define {name} ""{")
        self.__increment_indentation()
        self.run_scope(operator)
        self.__remove_indentation()
        self.print("}")

    def run_scope(self, operator: Scope):
        if operator.get_father() is None or isinstance(operator, FunctionScope):
            super().run_scope(operator)
        else:
            self.print("{")
            self.__increment_indentation()
            super().run_scope(operator)
            self.__remove_indentation()
            self.print("}")

    def run_datatype_declaration_operator(self, operator: DatatypeDeclarationOperation):
        self.print(f"%{operator.datatype} = {operator.creation};")

    def run_declaration_function(self, operator: DeclarationFunction):
        prename = ""
        postname = ""
        if isinstance(operator.function, GateOperation):
            prename = "__quantum__qis__"
            postname = "__body"
        self.print(f"declare {PrinterExecutor.__function_name(operator.function, prename, postname, with_register=False)};")

    def run(self, operator: Operation):
        super().run(operator)

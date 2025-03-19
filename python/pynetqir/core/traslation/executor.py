from abc import ABC, abstractmethod
from typing import Set

from python.pynetqir.core.operation import Operation, Function, ConditionalOperator
from python.pynetqir.core.operation.assembly import AllocateOperation, ICMPOperation, UnconditionalBranchOperation, \
    ConditionalBranchOperation
from python.pynetqir.core.operation.function import DeclarationFunction
from python.pynetqir.core.operation.scope import Scope, FunctionScope
from python.pynetqir.core.operation.utils import DatatypeDeclarationOperation


class Executor(ABC):

    def __init__(self):
        self.__functions_executed = set()
        self.__run_by_type = {
            SingleGateOperation: self.run_single_qubit_gate,
            MultipleGateOperation: self.run_multiple_qubit_gate,
            ControlledGateOperation: self.run_controlled_qubit_gate,
            ParameterizedGateOperation: self.run_parameterized_qubit_gate,
            ClassicalControlledGateOperation: self.run_classical_controlled_gate,
            MeasurementGateOperation: self.run_measurement_gate,
            ResetGateOperation: self.run_reset_gate,
            DatatypeDeclarationOperation: self.run_datatype_declaration_operator,
            ConditionalOperator: self.run_conditional_operator,
            AllocateOperation: self.run_allocate_operation,
            ICMPOperation: self.run_icmp_operation,
            UnconditionalBranchOperation: self.run_unconditional_branch_operation,
            ConditionalBranchOperation: self.run_conditional_branch_operation,
            DeclarationFunction: self.run_declaration_function,
            Function: self.run_function,
            FunctionScope: self.run_function_scope,
            Scope: self.run_scope,
        }

    @property
    def functions_executed(self):
        return self.__functions_executed

    @functions_executed.getter
    def functions_executed(self):
        return self.__functions_executed

    @property
    def run_by_type(self):
        return self.__run_by_type

    @run_by_type.getter
    def run_by_type(self):
        return self.__run_by_type

    @abstractmethod
    def run_single_qubit_gate(self, operator: SingleGateOperation):
        pass

    @abstractmethod
    def run_multiple_qubit_gate(self, operator: MultipleGateOperation):
        pass

    @abstractmethod
    def run_controlled_qubit_gate(self, operator: ControlledGateOperation):
        pass

    @abstractmethod
    def run_parameterized_qubit_gate(self, operator: ParameterizedGateOperation):
        pass

    @abstractmethod
    def run_measurement_gate(self, operator: MeasurementGateOperation):
        pass

    @abstractmethod
    def run_reset_gate(self, operator: ResetGateOperation):
        pass

    @abstractmethod
    def run_conditional_operator(self, operator: ConditionalOperator):
        pass

    @abstractmethod
    def run_function(self, operator: Function):
        pass

    @abstractmethod
    def run_allocate_operation(self, operator: AllocateOperation):
        pass

    @abstractmethod
    def run_icmp_operation(self, operator: ICMPOperation):
        pass

    @abstractmethod
    def run_unconditional_branch_operation(self, operator: UnconditionalBranchOperation):
        pass

    @abstractmethod
    def run_conditional_branch_operation(self, operator: ConditionalBranchOperation):
        pass

    @abstractmethod
    def run_function_scope(self, operator: FunctionScope):
        pass

    @abstractmethod
    def run_classical_controlled_gate(self, operator: ClassicalControlledGateOperation):
        pass

    @abstractmethod
    def run_declaration_function(self, operator: DeclarationFunction):
        pass

    @abstractmethod
    def run_datatype_declaration_operator(self, operator: DatatypeDeclarationOperation):
        pass

    def run_scope(self, operator: Scope):
        for op in operator.get_operations():
            self.run(op)

    def get_functions_executed(self) -> Set[Function]:
        return self.__functions_executed

    def run(self, operator: Operation):
        if isinstance(operator, Function):
            self.__functions_executed.add(operator)

        if type(operator) not in self.__run_by_type:
            # Check if the operator is instance of a class child of Function
            if issubclass(operator.__class__, Function):
                self.__run_by_type[Function](operator)
                return

            raise NotImplementedError(f"Operator {operator} (Class: {operator.__class__}) is not implemented")

        self.__run_by_type[type(operator)](operator)

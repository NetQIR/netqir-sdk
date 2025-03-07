from abc import ABC, abstractmethod

from pynetqir.core.operation import Operation, Function, ConditionalOperator
from pynetqir.core.operation.quantum.gates import *
from pynetqir.core.operation.scope import Scope


class Executor(ABC):

    def __init__(self):
        self.__functions_executed = set()
        self.__run_by_type = {
            SingleGateOperation: self.run_single_qubit_gate,
            MultipleGateOperation: self.run_multiple_qubit_gate,
            ControlledGateOperation: self.run_controlled_qubit_gate,
            ParameterizedGateOperation: self.run_parameterized_qubit_gate,
            MeasurementGateOperation: self.run_measurement_gate,
            ResetGateOperation: self.run_reset_gate,
            ConditionalOperator: self.run_conditional_operator,
            Function: self.run_function,
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

    def run_scope(self, operator: Scope):
        for op in operator.operators:
            self.run(op)

    def run(self, operator: Operation):
        if isinstance(operator, Function):
            self.__functions_executed.add(operator)

        # Assert if operator is in the run_by_type dictionary
        assert type(operator) in self.__run_by_type.keys(), f"Operator {operator} is not in the run_by_type dictionary"
        self.__run_by_type[type(operator)](operator)

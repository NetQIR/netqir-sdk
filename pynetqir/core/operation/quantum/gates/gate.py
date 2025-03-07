from abc import ABC, abstractmethod
from typing import List

from pynetqir.core.operation import Function, Parameter
from pynetqir.datatypes.qir import Qubit, Result


class GateOperation(Function, ABC):

    @abstractmethod
    def __init__(self, name: str, parameters: List[Parameter]):
        super().__init__(name, "void", parameters)
        pass


class SingleGateOperation(GateOperation):
    def __init__(self, name: str, qubit: Qubit):
        super().__init__(name, [Parameter(qubit, qubit.datatype())])
        self.__qubit = qubit


class MultipleGateOperation(GateOperation):
    def __init__(self, name: str, qubits: List[Qubit]):
        super().__init__(name, [Parameter(q, q.datatype()) for q in qubits])
        self.__qubits = qubits


class ControlledGateOperation(GateOperation):
    def __init__(self, name: str, controls: List[Qubit], targets: List[Qubit]):
        super().__init__(name, [Parameter(q, q.datatype()) for q in controls + targets])
        self.__controls = controls
        self.__targets = targets


class ParameterizedGateOperation(GateOperation):
    def __init__(self, name: str, qubit: Qubit, parameters: List[float]):
        super().__init__(name, [Parameter(qubit, qubit.datatype())] + [Parameter(f"{i}", "double") for i in
                                                                       range(len(parameters))])
        self.__qubit = qubit
        self.__parameters = parameters


class MeasurementGateOperation(GateOperation):
    def __init__(self, qubit: Qubit, result: Result):
        super().__init__("mz", [Parameter(qubit, qubit.datatype()), Parameter(result, result.datatype())])
        self.__qubit = qubit


class ResetGateOperation(GateOperation):
    def __init__(self, qubit: Qubit):
        super().__init__("reset", [Parameter(qubit, qubit.datatype())])
        self.__qubit = qubit

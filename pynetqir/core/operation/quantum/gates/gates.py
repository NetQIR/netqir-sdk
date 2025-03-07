from typing import Callable

from pynetqir.core.operation.quantum.gates import MeasurementGateOperation, ResetGateOperation
from pynetqir.core.operation.quantum.gates.gate import SingleGateOperation, ControlledGateOperation, \
    ParameterizedGateOperation
from pynetqir.datatypes.qir import Result, Qubit
from pynetqir.core.traslation import Printer


class QuantumGates:
    """
    A class to represent various quantum gates and operations.

    This class provides static methods to apply different quantum gates and operations
    on qubits. It includes single-qubit gates, multi-qubit gates, parameterized gates,
    and other quantum operations such as measurement and reset. The gates and operations
    are translated to NetQIR using the Printer class.
    """
    def __init__(self):
        pass

    @staticmethod
    def I(qubit: Qubit):
        """Identity gate"""
        return SingleGateOperation("I", qubit)

    @staticmethod
    def X(qubit: Qubit):
        """Pauli-X (NOT) gate"""
        return SingleGateOperation("X", qubit)

    @staticmethod
    def Y(qubit: Qubit):
        """Pauli-Y gate"""
        return SingleGateOperation("Y", qubit)

    @staticmethod
    def Z(qubit: Qubit):
        """Pauli-Z gate"""
        return SingleGateOperation("Z", qubit)

    @staticmethod
    def H(qubit: Qubit):
        """Hadamard gate"""
        return SingleGateOperation("H", qubit)

    @staticmethod
    def S(qubit: Qubit):
        """Phase gate"""
        return SingleGateOperation("S", qubit)

    @staticmethod
    def T(qubit: Qubit):
        """T gate (π/8 gate)"""
        return SingleGateOperation("T", qubit)

    @staticmethod
    def CNOT(control: Qubit, target: Qubit):
        """Controlled-NOT (CNOT) gate"""
        return ControlledGateOperation("CNOT", [control], [target])

    @staticmethod
    def CZ(control: Qubit, target: Qubit):
        """Controlled-Z gate"""
        return ControlledGateOperation("CZ", [control], [target])

    @staticmethod
    def SWAP(control: Qubit, target: Qubit):
        """SWAP gate"""
        return ControlledGateOperation("SWAP", [control], [target])

    @staticmethod
    def RX(theta, qubit: Qubit):
        """Rotation around X-axis"""
        return ParameterizedGateOperation("RX", qubit, [theta])

    @staticmethod
    def RY(theta, qubit: Qubit):
        """Rotation around Y-axis"""
        return ParameterizedGateOperation("RY", qubit, [theta])

    @staticmethod
    def RZ(theta, qubit: Qubit):
        """Rotation around Z-axis"""
        return ParameterizedGateOperation("RZ", qubit, [theta])

    @staticmethod
    def ccx(control1: Qubit, control2: Qubit, target: Qubit):
        """Toffoli (CCX) gate"""
        return ControlledGateOperation("CCX", [control1, control2], [target])

    @staticmethod
    def mz(qubit: Qubit, result: Result):
        """Measurement in Z basis"""
        return MeasurementGateOperation(qubit, result)

    @staticmethod
    def reset(qubit: Qubit):
        """Reset gate"""
        return ResetGateOperation(qubit)

    @staticmethod
    def s_adj(qubit: Qubit):
        """Adjoint of Phase gate"""
        return SingleGateOperation("S_ADJ", qubit)

    @staticmethod
    def t_adj(qubit: Qubit):
        """Adjoint of T gate"""
        return SingleGateOperation("T_ADJ", qubit)

    @staticmethod
    def if_result(cond, qubit: Qubit,
                  one: Callable[[Qubit], None],
                  zero: Callable[[Qubit], None]):
        """Conditional gate based on measurement result"""
        Printer.get_printer().print_conditional_gate(one, zero, qubit, cond)

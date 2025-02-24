from typing import Callable
from PyNetQIR.classical import Result
from PyNetQIR.quantum import Qubit
from PyNetQIR.core import Printer


class QuantumGate:
    def __init__(self):
        pass

    @staticmethod
    def I(qubit: Qubit):
        """Identity gate"""
        Printer.get_printer().print_single_gate("I", qubit)

    @staticmethod
    def X(qubit: Qubit):
        """Pauli-X (NOT) gate"""
        Printer.get_printer().print_single_gate("X", qubit)

    @staticmethod
    def Y(qubit: Qubit):
        """Pauli-Y gate"""
        Printer.get_printer().print_single_gate("Y", qubit)

    @staticmethod
    def Z(qubit: Qubit):
        """Pauli-Z gate"""
        Printer.get_printer().print_single_gate("Z", qubit)

    @staticmethod
    def H(qubit: Qubit):
        """Hadamard gate"""
        Printer.get_printer().print_single_gate("H", qubit)

    @staticmethod
    def S(qubit: Qubit):
        """Phase gate"""
        Printer.get_printer().print_single_gate("S", qubit)

    @staticmethod
    def T(qubit: Qubit):
        """T gate (π/8 gate)"""
        Printer.get_printer().print_single_gate("T", qubit)

    @staticmethod
    def CNOT(control: Qubit, target: Qubit):
        """Controlled-NOT (CNOT) gate"""
        Printer.get_printer().print_two_qubit_gate("CNOT", control, target)

    @staticmethod
    def CZ(control: Qubit, target: Qubit):
        """Controlled-Z gate"""
        Printer.get_printer().print_two_qubit_gate("CZ", control, target)

    @staticmethod
    def SWAP(control: Qubit, target: Qubit):
        """SWAP gate"""
        Printer.get_printer().print_two_qubit_gate("SWAP", control, target)

    @staticmethod
    def RX(theta, qubit: Qubit):
        """Rotation around X-axis"""
        Printer.get_printer().print_param_gate("RX", theta, qubit)

    @staticmethod
    def RY(theta, qubit: Qubit):
        """Rotation around Y-axis"""
        Printer.get_printer().print_param_gate("RY", theta, qubit)

    @staticmethod
    def RZ(theta, qubit: Qubit):
        """Rotation around Z-axis"""
        Printer.get_printer().print_param_gate("RZ", theta, qubit)

    @staticmethod
    def barrier():
        """Barrier gate"""
        Printer.get_printer().print_barrier()

    @staticmethod
    def ccx(control1: Qubit, control2: Qubit, target: Qubit):
        """Toffoli (CCX) gate"""
        Printer.get_printer().print_three_qubit_gate("CCX", control1, control2, target)

    @staticmethod
    def mz(qubit: Qubit, result: Result):
        """Measurement in Z basis"""
        return Printer.get_printer().print_measurement(qubit, result)

    @staticmethod
    def reset(qubit: Qubit):
        """Reset gate"""
        Printer.get_printer().print_single_gate("RESET", qubit)

    @staticmethod
    def s_adj(qubit: Qubit):
        """Adjoint of Phase gate"""
        Printer.get_printer().print_single_gate("S_ADJ", qubit)

    @staticmethod
    def t_adj(qubit: Qubit):
        """Adjoint of T gate"""
        Printer.get_printer().print_single_gate("T_ADJ", qubit)

    @staticmethod
    def if_result(cond, qubit: Qubit,
                  one: Callable[[Qubit], None],
                  zero: Callable[[Qubit], None]):
        """Conditional gate based on measurement result"""
        Printer.get_printer().print_conditional_gate(one, zero, qubit, cond)

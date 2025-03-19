from python.pynetqir.core.operation.quantum.gates import MeasurementGateOperation, ResetGateOperation, \
    ClassicalControlledGateOperation
from python.pynetqir.core.operation.quantum.gates.gate import SingleGateOperation, ControlledGateOperation, \
    ParameterizedGateOperation
from python.pynetqir.datatypes.qir import Result, Qubit

from enum import Enum


class GateType(Enum):
    SINGLE_GATE = 1
    CONTROLLED_GATE = 2
    PARAMETERIZED_GATE = 3


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

    single_gates = {"I", "X", "Y", "Z", "H", "S", "T", "S_ADJ", "T_ADJ"}
    controlled_gates = {"CNOT", "CZ", "SWAP", "CCX"}
    parameterized_gates = {"RX", "RY", "RZ"}

    @staticmethod
    def generate_gate_method(gate_name, type: GateType):
        def single_gate_method(qubit):
            """Dynamically generated gate method"""
            return SingleGateOperation(gate_name, qubit)

        def controlled_gate_method(control, target):
            """Dynamically generated controlled gate method"""
            return ControlledGateOperation(gate_name, [control], [target])

        def parameterized_gate_method(qubit, *parameters):
            """Dynamically generated parameterized gate method"""
            return ParameterizedGateOperation(gate_name, qubit, list(parameters))

        gate_methods = {GateType.SINGLE_GATE: single_gate_method,
                        GateType.CONTROLLED_GATE: controlled_gate_method,
                        GateType.PARAMETERIZED_GATE: parameterized_gate_method}

        gate_method = gate_methods[type]

        gate_method.__name__ = gate_name
        gate_method.__doc__ = f"{gate_name} gate"
        return staticmethod(gate_method)

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
    def classical_controlled(control_reg: Result, c_gate: SingleGateOperation):
        """Classical controlled gate"""
        return ClassicalControlledGateOperation(control_reg, c_gate)


# Generation of functions for each gate
for gate in QuantumGates.single_gates:
    setattr(QuantumGates, gate, QuantumGates.generate_gate_method(gate, GateType.SINGLE_GATE))

for gate in QuantumGates.controlled_gates:
    setattr(QuantumGates, gate, QuantumGates.generate_gate_method(gate, GateType.CONTROLLED_GATE))

for gate in QuantumGates.parameterized_gates:
    setattr(QuantumGates, gate, QuantumGates.generate_gate_method(gate, GateType.PARAMETERIZED_GATE))

    # @staticmethod
    # def I(qubit: Qubit):
    #     """Identity gate"""
    #     return SingleGateOperation("I", qubit)
    #
    # @staticmethod
    # def X(qubit: Qubit):
    #     """Pauli-X (NOT) gate"""
    #     return SingleGateOperation("X", qubit)
    #
    # @staticmethod
    # def Y(qubit: Qubit):
    #     """Pauli-Y gate"""
    #     return SingleGateOperation("Y", qubit)
    #
    # @staticmethod
    # def Z(qubit: Qubit):
    #     """Pauli-Z gate"""
    #     return SingleGateOperation("Z", qubit)
    #
    # @staticmethod
    # def H(qubit: Qubit):
    #     """Hadamard gate"""
    #     return SingleGateOperation("H", qubit)
    #
    # @staticmethod
    # def S(qubit: Qubit):
    #     """Phase gate"""
    #     return SingleGateOperation("S", qubit)
    #
    # @staticmethod
    # def T(qubit: Qubit):
    #     """T gate (π/8 gate)"""
    #     return SingleGateOperation("T", qubit)
    #
    #
    # @staticmethod
    # def CNOT(control: Qubit, target: Qubit):
    #     """Controlled-NOT (CNOT) gate"""
    #     return ControlledGateOperation("CNOT", [control], [target])
    #
    # @staticmethod
    # def CZ(control: Qubit, target: Qubit):
    #     """Controlled-Z gate"""
    #     return ControlledGateOperation("CZ", [control], [target])
    #
    # @staticmethod
    # def SWAP(control: Qubit, target: Qubit):
    #     """SWAP gate"""
    #     return ControlledGateOperation("SWAP", [control], [target])
    #
    #
    # @staticmethod
    # def RX(theta, qubit: Qubit):
    #     """Rotation around X-axis"""
    #     return ParameterizedGateOperation("RX", qubit, [theta])
    #
    # @staticmethod
    # def RY(theta, qubit: Qubit):
    #     """Rotation around Y-axis"""
    #     return ParameterizedGateOperation("RY", qubit, [theta])
    #
    # @staticmethod
    # def RZ(theta, qubit: Qubit):
    #     """Rotation around Z-axis"""
    #     return ParameterizedGateOperation("RZ", qubit, [theta])

    # @staticmethod
    # def s_adj(qubit: Qubit):
    #     """Adjoint of Phase gate"""
    #     return SingleGateOperation("S_ADJ", qubit)
    #
    # @staticmethod
    # def t_adj(qubit: Qubit):
    #     """Adjoint of T gate"""
    #     return SingleGateOperation("T_ADJ", qubit)

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

    single_gates = {"i", "x", "y", "z", "h", "s", "t", "s_adj", "t_adj"}
    controlled_gates = {"cx", "cz", "swap"}
    parameterized_gates = {"rx", "ry", "rz"}

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
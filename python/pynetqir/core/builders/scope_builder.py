from collections.abc import Callable
from typing import List

from python.pynetqir.core.operation import Function, Parameter, ConditionalOperator, Operation
from python.pynetqir.core.operation.assembly import AllocateOperation, ICMPOperation, ConditionalBranchOperation, \
    UnconditionalBranchOperation
from python.pynetqir.core.operation.assembly.br import TagMarkerOperation
from python.pynetqir.core.operation.conditional import ConditionalType
from python.pynetqir.core.operation.quantum.gates import SingleGateOperation, ControlledGateOperation, \
    ParameterizedGateOperation, MeasurementGateOperation, ResetGateOperation, ClassicalControlledGateOperation, \
    GateOperation
from python.pynetqir.core.operation.quantum.gates.gates import QuantumGates, GateType
from python.pynetqir.core.operation.quantum.netqir import NetQIROperations
from python.pynetqir.core.operation.quantum.netqir.state import Initialize, Finalize
from python.pynetqir.core.operation.scope import Scope, FunctionScope
from python.pynetqir.datatypes import Register, TemporalRegister
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister
from python.pynetqir.datatypes.netqir.rank import InmediateRank, Rank
from python.pynetqir.datatypes.qir import Qubit, Result


class ScopeBuilder:
    def __init__(self, n_qubits: int, n_results: int):
        self.operations = list()
        self.qubits = None
        self.results = None
        self.__build(n_qubits, n_results)

    def __build(self, n_qubits: int, n_results: int):
        self.qubits, q_operations = AllocateOperation.allocate_register(n_qubits, Qubit)
        self.results, r_operations = AllocateOperation.allocate_register(n_results, Result)

        self._add_operations(q_operations + r_operations)

    def build(self, parent: Scope = None) -> Scope:
        return Scope(parent=parent, operations=self.operations)

    def ccx(self, control1_idx: int, control2_idx: int, target_idx: int) -> 'ScopeBuilder':
        """Toffoli (CCX) gate"""
        control1 = self.get_qubit(control1_idx)
        control2 = self.get_qubit(control2_idx)
        target = self.get_qubit(target_idx)
        operation = ControlledGateOperation("ccx", [control1, control2], [target])
        self._add_operation(operation)

        return self

    def mz(self, qidx: int, result_idx: int) -> 'ScopeBuilder':
        """Measurement in Z basis"""
        # Get the qubit and result registers
        qubit = self.get_qubit(qidx)
        result = self.get_result(result_idx)

        operation = MeasurementGateOperation(qubit, result)
        self._add_operation(operation)

        return self

    def reset(self, qidx: int) -> 'ScopeBuilder':
        """Reset gate"""
        qubit = self.get_qubit(qidx)

        self._add_operation(ResetGateOperation(qubit))

        return self

    def classical_controlled(self, control_reg_idx: int, c_gate: callable) -> 'ScopeBuilder':
        """Classical controlled gate"""
        result = self.get_result(control_reg_idx)
        self.conditional(ConditionalType.EQUAL, result, InmediateRank(1), [c_gate], [])
        return self

    # ConditionalOperator(ConditionalType.EQUAL, my_rank, InmediateRank(0),
    #                                        [NetQIROperations.qsend(comm_world, qreg[0], InmediateRank(1))],
    #                                        [NetQIROperations.qrecv(comm_world, qreg[1], InmediateRank(0))]))

    def conditional(self, condition: ConditionalType,
                    left_register: Register, right_register: Register,
                    true_operations: List[callable],
                    false_operations: List[callable]) -> 'ScopeBuilder':

        # ICMP operation
        tmp_result = TemporalRegister("_result")
        tmp_true_branch = TemporalRegister("_true")
        tmp_false_branch = TemporalRegister("_false")
        tmp_continue_branch = TemporalRegister("_continue")
        self._add_operation(ICMPOperation(condition, left_register, right_register, tmp_result))
        self._add_operation(ConditionalBranchOperation(tmp_result, tmp_true_branch, tmp_false_branch))

        # True branch
        self._add_operation(TagMarkerOperation(tmp_true_branch))
        # call the true operations
        for operation in true_operations:
            operation()

        self._add_operation(UnconditionalBranchOperation(tmp_continue_branch))

        # False branch
        self._add_operation(TagMarkerOperation(tmp_false_branch))
        # call the false operations
        for operation in false_operations:
            operation()

        self._add_operation(UnconditionalBranchOperation(tmp_continue_branch))

        # Continue branch
        self._add_operation(TagMarkerOperation(tmp_continue_branch))

        return self

    def call(self, function: Function, *args) -> 'ScopeBuilder':
        parameters = function.parameters
        assert len(args) == len(
            parameters), f"Number of arguments {len(args)} does not match the number of parameters {len(parameters)} for the Function {function.name}"

        new_parameters = []
        for arg, parameter in zip(args, parameters):
            if parameter.type == Qubit.datatype_default():
                new_parameters.append(Parameter(register=self.get_qubit(arg)))
            elif parameter.type == Result.datatype_default():
                new_parameters.append(Parameter(register=self.get_result(arg)))
            else:
                new_parameters.append(parameter)

        function = Function(function.name, function.return_type, new_parameters, function.return_register)
        self._add_operation(function)
        return self

    def get_qubit(self, idx: int) -> Qubit:
        assert len(self.qubits) > idx >= 0, f"Qubit index {idx} out of range of the scope"
        return self.qubits[idx]

    def get_result(self, idx: int) -> Result:
        assert len(self.results) > idx >= 0, f"Result index {idx} out of range of the scope"
        return self.results[idx]

    """
    NetQIR Operations
    """

    #
    # State operations
    #
    def netqir_initialize(self):
        self._add_operation(Initialize())
        return self

    def netqir_finalize(self):
        self._add_operation(Finalize())
        return self

    #
    # Operate datatypes
    #
    def get_rank(self, comm: CommunicatorRegister) -> Rank:
        rank, operations = NetQIROperations.get_rank(comm)
        self._add_operations(operations)
        return rank

    def get_comm_size(self, comm: CommunicatorRegister, register: Register) -> 'ScopeBuilder':
        operation = NetQIROperations.get_comm_size(comm, register)
        self._add_operation(operation)
        return self

    #
    # Communication operations
    #
    def qsend(self, comm: CommunicatorRegister, qidx: int, dest: int) -> 'ScopeBuilder':
        """Send a qubit to a destination"""
        qubit = self.get_qubit(qidx)
        self._add_operation(NetQIROperations.qsend(comm, qubit, InmediateRank(dest)))
        return self

    def qrecv(self, comm: CommunicatorRegister, qidx: int, source: int) -> 'ScopeBuilder':
        """Receive a qubit from a source"""
        qubit = self.get_qubit(qidx)
        self._add_operation(NetQIROperations.qrecv(comm, qubit, InmediateRank(source)))
        return self

    """
    Stub definition for the following methods:
    1. Single-qubit gates
    2. Controlled / multi-qubit gates
    3. Parameterized rotation gates
    
    The methods are dynamically generated using the _generate_gate_method method. The definition is only for the IntelliSense
    to work properly.
    """

    # Single-qubit gates
    def i(self, qidx: int) -> 'ScopeBuilder':
        """I gate applied to a single qubit."""
        pass

    def x(self, qidx: int) -> 'ScopeBuilder':
        """X gate applied to a single qubit."""
        pass

    def y(self, qidx: int) -> 'ScopeBuilder':
        """Y gate applied to a single qubit."""
        pass

    def z(self, qidx: int) -> 'ScopeBuilder':
        """Z gate applied to a single qubit."""
        pass

    def h(self, qidx: int) -> 'ScopeBuilder':
        """H gate applied to a single qubit."""
        pass

    def s(self, qidx: int) -> 'ScopeBuilder':
        """S gate applied to a single qubit."""
        pass

    def t(self, qidx: int) -> 'ScopeBuilder':
        """T gate applied to a single qubit."""
        pass

    def s_adj(self, qidx: int) -> 'ScopeBuilder':
        """S† (S dagger) gate applied to a single qubit."""
        pass

    def t_adj(self, qidx: int) -> 'ScopeBuilder':
        """T† (T dagger) gate applied to a single qubit."""
        pass

    # Controlled / multi-qubit gates
    def cx(self, control: int, target: int) -> 'ScopeBuilder':
        """Controlled-X (CNOT) gate between control and target qubits."""
        pass

    def cz(self, control: int, target: int) -> 'ScopeBuilder':
        """Controlled-Z gate between control and target qubits."""
        pass

    def swap(self, q1: int, q2: int) -> 'ScopeBuilder':
        """SWAP gate between two qubits."""
        pass

    # Parameterized rotation gates
    def rx(self, qidx: int, theta: float) -> 'ScopeBuilder':
        """Rotation around X-axis by angle theta."""
        pass

    def ry(self, qidx: int, theta: float) -> 'ScopeBuilder':
        """Rotation around Y-axis by angle theta."""
        pass

    def rz(self, qidx: int, theta: float) -> 'ScopeBuilder':
        """Rotation around Z-axis by angle theta."""
        pass

    def _add_operations(self, operations):
        self.operations.extend(operations)

    def _add_operation(self, operation):
        self.operations.append(operation)

    @staticmethod
    def _generate_gate_method(gate_name, type: GateType):
        def single_gate_method(self, qidx: int) -> 'ScopeBuilder':
            """Dynamically generated gate method"""
            qubit = self.get_qubit(qidx)

            operation = SingleGateOperation(gate_name, qubit)
            self._add_operation(operation)

            return self

        def controlled_gate_method(self, control_idx: int, target_idx: int) -> 'ScopeBuilder':
            """Dynamically generated controlled gate method"""
            control = self.get_qubit(control_idx)
            target = self.get_qubit(target_idx)

            operation = ControlledGateOperation(gate_name, [control], [target])
            self._add_operation(operation)

            return self

        def parameterized_gate_method(self, qidx: int, *parameters) -> 'ScopeBuilder':
            """Dynamically generated parameterized gate method"""
            qubit = self.get_qubit(qidx)
            operation = ParameterizedGateOperation(gate_name, qubit, list(parameters))
            self._add_operation(operation)

            return self

        gate_methods = {GateType.SINGLE_GATE: single_gate_method,
                        GateType.CONTROLLED_GATE: controlled_gate_method,
                        GateType.PARAMETERIZED_GATE: parameterized_gate_method}

        gate_method = gate_methods[type]

        gate_method.__name__ = gate_name
        return gate_method


for gate in QuantumGates.single_gates:
    setattr(ScopeBuilder, gate, ScopeBuilder._generate_gate_method(gate, GateType.SINGLE_GATE))

for gate in QuantumGates.controlled_gates:
    setattr(ScopeBuilder, gate, ScopeBuilder._generate_gate_method(gate, GateType.CONTROLLED_GATE))

for gate in QuantumGates.parameterized_gates:
    setattr(ScopeBuilder, gate, ScopeBuilder._generate_gate_method(gate, GateType.PARAMETERIZED_GATE))


class FunctionScopeBuilder(ScopeBuilder):
    def __init__(self, n_qubits: int, n_results: int, function: Function = None):
        # Get the number of parameters with type Qubit
        qubits_registers = [parameter.register for parameter in function.parameters if
                            parameter.register is not None and parameter.register.datatype_default() == Qubit.datatype_default()]

        result_registers = [parameter.register for parameter in function.parameters if
                            parameter.register is not None and parameter.register.datatype_default() == Result.datatype_default()]

        # Initialize the ScopeBuilder with the number of qubits and results minus the number of qubits and results
        # already defined in the function parameters
        super().__init__(n_qubits - len(qubits_registers), n_results - len(result_registers))

        self.qubits = qubits_registers + [q for q in self.qubits]
        self.results = result_registers + [r for r in self.results]

        # Allocate the qubits and results
        allocate_qubits = [AllocateOperation(register) for register in qubits_registers]
        allocate_results = [AllocateOperation(register) for register in result_registers]

        super()._add_operations(allocate_qubits + allocate_results)

        self.function = function

    def set_function(self, function: Function):
        self.function = function
        return self

    def build(self, parent: Scope = None) -> Scope:
        assert self.function is not None, "Function not set"
        return FunctionScope(parent=parent, function=self.function, operations=self.operations)


class MainScopeBuilder(FunctionScopeBuilder):
    def __init__(self, n_qubits: int, n_results: int):
        super().__init__(n_qubits, n_results, Function("main"))

    def build(self, parent: Scope = None) -> Scope:
        return super().build(parent=parent)

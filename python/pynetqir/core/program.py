from python.pynetqir.core.operation.assembly import AllocateOperation
from python.pynetqir.core.operation.function import DeclarationFunction, Function
from python.pynetqir.core.operation.scope import Scope, FunctionScope
from python.pynetqir.core.operation.utils import DatatypeDeclarationOperation
from python.pynetqir.core.traslation import Executor
from python.pynetqir.core.traslation.executors import PrinterExecutor
from python.pynetqir.datatypes.netqir.communicator import CommunicatorRegister, NamedCommunicatorRegister
from python.pynetqir.datatypes.qir import Qubit, Result
from python.pynetqir.datatypes.register import NamedRegister


class Program:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Program, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name="main", executor: Executor = None):
        self.name = name
        self.global_scope = Scope()
        self.executor = executor
        self.size_world_register = NamedRegister("size_world")
        self.comm_world = NamedCommunicatorRegister("netqir_comm_world")

        if self.executor is None:
            self.executor = PrinterExecutor()

    def get_global_scope(self) -> 'Scope':
        return self.global_scope

    def get_size_world_register(self):
        return self.size_world_register

    def get_comm_world(self) -> CommunicatorRegister:
        return self.comm_world

    @staticmethod
    def get_instance():
        return Program._instance

    def start(self):
        self.global_scope.add_operations(
            [
                DatatypeDeclarationOperation(Qubit.__name__),
                DatatypeDeclarationOperation(Result.__name__),
                DatatypeDeclarationOperation('Comm'),
                AllocateOperation(self.size_world_register)
            ]
        )
        pass

    def run(self):
        self.executor.run(self.global_scope)

    def end(self):
        func_executed = self.executor.get_functions_executed()

        for f in func_executed:
            self.executor.run(DeclarationFunction(f))
        pass

from pynetqir.core.operation.scope import Scope
from pynetqir.core.traslation import PrinterExecutor
from pynetqir.datatypes.qir import Qubit, Result


class Program:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Program, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name="main", num_qubits=1, num_results=1):
        self.name = name
        self.global_scope = Scope()

        self.num_qubits = num_qubits
        self.qubits = [Qubit() for _ in range(num_qubits)]

        self.num_results = num_results
        self.results = [Result() for _ in range(num_results)]

        self.executor = PrinterExecutor()

    def get_global_scope(self):
        return self.global_scope

    @staticmethod
    def get_instance():
        return Program._instance

    def start(self):
        # TODO - Aquí se añaden instrucciones alloca al global scope para los qubits y los resultados
        # TODO - el executor tiene una función que sea initialize y finish
        pass

    def run(self):
        self.executor.run(self.global_scope)
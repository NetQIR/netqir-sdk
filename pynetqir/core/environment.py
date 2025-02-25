from typing import List
from pynetqir.core import Printer
from pynetqir.quantum import Qubit
from pynetqir.classical import Result
from pynetqir.communication.utils import Rank


class Environment:
    """
    A class to represent a quantum computing environment.
    Attributes:
    ----------
    num_qubits : int
        The number of qubits in the environment.
    qubits : list
        A list of Qubit objects representing the qubits in the environment.
    results : list
        A list of Result objects representing the results in the environment.
    printer : Printer
        A Printer object used to translate state to a NetQIR code.

    Methods
    -------
    __init__(name, num_qubits, num_results)
        Initializes the environment with the given number of qubits and results, and sets up the printer.
    get_qubits()
        Returns the list of qubits in the environment.
    get_results()
        Returns the list of results in the environment.
    finalize()
        Finalizes the environment by closing the printer function and the printer itself.
    """

    def __init__(self, name, num_qubits: int, num_results: int):
        self.num_qubits = num_qubits

        self.qubits = [Qubit() for _ in range(num_qubits)]

        self.results = [Result() for _ in range(num_results)]

        self.printer = Printer(f"{name}.ll")
        self.printer.print_initialize()

        # Allocate qubits
        for j in range(num_qubits):
            self.printer.print_alloca(self.qubits[j], Qubit.__name__)

        for j in range(num_results):
            self.printer.print_alloca(self.results[j], Result.__name__)

    def get_qubits(self):
        return self.qubits

    def get_results(self):
        return self.results

    def finalize(self):
        self.printer.close_function()
        self.printer.print_blank_line()
        self.printer.declarate_functions()
        self.printer.close()

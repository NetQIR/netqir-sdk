from typing import List
from PyNetQIR.core import Printer
from PyNetQIR.quantum import Qubit
from PyNetQIR.classical import Result
from PyNetQIR.communication.utils import Rank

class Environment:
    def __init__(self, name, num_nodes: int, num_qubits: List[int], num_results: List[int]):
        self.num_nodes = num_nodes
        self.num_qubits = num_qubits

        self.qubits = [[Qubit() for _ in range(num_qubits[i])]
                       for i in range(num_nodes)]

        self.results = [[Result() for _ in range(num_results[i])]
                        for i in range(num_nodes)]
        
        self.ranks = [Rank() for _ in range(num_nodes)]

        self.printer = Printer(f"{name}.ll")

    def get_qubits(self, node: int):
        return self.qubits[node]
    
    def get_results(self, node: int):
        return self.results[node]
    
    def get_ranks(self):
        return self.ranks
    
    def finalize(self):
        self.printer.close()
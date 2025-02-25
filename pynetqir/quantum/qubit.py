class Qubit:
    total_qubits = 0

    def __init__(self):
        self.identifier = Qubit.total_qubits
        Qubit.total_qubits += 1
        
    def __repr__(self):
        return f"%q{self.identifier}"
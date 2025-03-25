from python.pynetqir.core.operation import Operation
from python.pynetqir.datatypes import TemporalRegister, Register


class UnconditionalBranchOperation(Operation):
    def __init__(self, label: TemporalRegister):
        super().__init__()
        self.label = label

    def __str__(self):
        return f"br label {self.label}"

class ConditionalBranchOperation(Operation):
    def __init__(self, condition: Register, true_label: TemporalRegister, false_label: TemporalRegister):
        super().__init__()
        self.condition = condition
        self.true_label = true_label
        self.false_label = false_label

    def __str__(self):
        return f"br i1 {self.condition}, label {self.true_label}, label {self.false_label}"

class TagMarkerOperation(Operation):
    def __init__(self, tag: str):
        super().__init__()
        self.tag = tag

    def __str__(self):
        return f"{self.tag}:"
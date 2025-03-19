from python.pynetqir.core.operation import Operation
from enum import Enum
from typing import List

from python.pynetqir.datatypes import Register


class ConditionalType(Enum):
    EQUAL = "eq",
    NOT_EQUAL = "ne",
    GREATER = "gt",
    GREATER_EQUAL = "ge",
    LESS = "lt",
    LESS_EQUAL = "le"

    def __str__(self):
        return self.value[0]


class ConditionalOperator(Operation):

    def __init__(self, comm_type: ConditionalType,
                 left: Register, right: Register,
                 operators_true: List[Operation],
                 operators_false: List[Operation]):
        super().__init__()
        self.comm_type = comm_type
        self.left = left
        self.right = right
        self.operators_true = operators_true
        self.operators_false = operators_false


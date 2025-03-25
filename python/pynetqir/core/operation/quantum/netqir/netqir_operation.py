from abc import ABC
from typing import List

from python.pynetqir.core.operation import Function, Parameter

class NetQIROperation(Function, ABC):
    def __init__(self, name: str, parameters: List[Parameter] = []):
        super().__init__(f"__netqir__{name}", parameters=parameters, return_type="i32")



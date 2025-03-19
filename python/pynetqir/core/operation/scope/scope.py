from typing import List

from python.pynetqir.core.operation import Operation


class Scope(Operation):

    def __init__(self, parent = None):

        # Father is the parent Scope object of this current Scope object
        self.__father = parent
        
        """
        Generation and Children ID compose the ID of the Scope object.
        """
        # Generation it's the level of the scope in the tree.
        self.__generation = 0

        # Children ID is the index of the child in the list of children of the father
        self.__children_id = 0
        
        # List of the children of the current Scope object
        self.__children = []

        # Queue of operations to be executed
        self.__operations = list()

        if parent is not None:
            parent.append_child(self)

    def __get_id(self):
        return f'G{self.__generation}.C{self.__children_id}'

    def __add_child(self, child: 'Scope'):
        self.__children.append(child)

    def __add_operation(self, operation: Operation):
        self.__operations.append(operation)

    def __str__(self):
        return self.__get_id()

    def append_child(self, child: 'Scope'):
        child.__father = self
        child.__generation = self.__generation + 1
        child.__children_id = len(self.__children)
        self.__add_child(child)

        # Append the Scope object to the list of operations to be executed
        self.__add_operation(child)
        return child

    def give_birth(self):
        return Scope(self)

    def add_operation(self, operation: Operation):
        self.__add_operation(operation)

    def add_operations(self, operations: List[Operation]):
        for operation in operations:
            self.__add_operation(operation)

    def get_operations(self) -> List[Operation]:
        return self.__operations

    def get_children(self) -> List['Scope']:
        return self.__children

    def get_father(self) -> 'Scope':
        return self.__father
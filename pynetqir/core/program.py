from pynetqir.core import Scope

class Program:

    _instance = None
    GLOBAL_SCOPE = Scope()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Program, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    @staticmethod
    def get_instance():
        return Program._instance
    
    @staticmethod
    def get_global_scope():
        return Program.GLOBAL_SCOPE
    


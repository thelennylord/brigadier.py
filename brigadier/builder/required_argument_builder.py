from brigadier.tree import ArgumentCommandNode

from .argument_builder import ArgumentBuilder


class RequiredArgumentBuilder(ArgumentBuilder):
    def __init__(self, name, arg_type):
        super().__init__()
        self.name = name
        self.type = arg_type

        self.suggestions_provider = None
       
    def suggests(self, provider):
        self.suggestions_provider = provider
        return self.get_self()
    
    def get_self(self):
        return self
    
    def get_type(self):
        return self.type
    
    def get_name(self):
        return self.name
    
    def get_suggestions_provider(self):
        return self.suggestions_provider
    
    def build(self):
        result = ArgumentCommandNode(self.get_name(), self.get_type(), self.get_command(), self.get_requirement(), self.get_redirect(), self.get_redirect_modifier(), self.is_fork(), self.get_suggestions_provider())
        for argument in self.get_arguments():
                result.add_child(argument)
        return result

def argument(name, arg_type):
    return RequiredArgumentBuilder(name, arg_type)

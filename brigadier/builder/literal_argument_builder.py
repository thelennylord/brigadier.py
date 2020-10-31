from .argument_builder import ArgumentBuilder


class LiteralArgumentBuilder(ArgumentBuilder):
    def __init__(self, literal):
        super().__init__()
        self.literal = literal
    
    def get_self(self):
        return self
    
    def get_literal(self):
        return self.literal
    
    def build(self):
        from brigadier.tree import LiteralCommandNode
        
        result = LiteralCommandNode(self.get_literal(), self.get_command(), self.get_requirement(), self.get_redirect(), self.get_redirect_modifier(), self.is_fork())
        for argument in self.get_arguments():
            result.add_child(argument)
        return result

def literal(name):
    return LiteralArgumentBuilder(name)

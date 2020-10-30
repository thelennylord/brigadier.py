from brigadier.suggestion import empty_suggestion
from brigadier.tree import CommandNode


class RootCommandNode(CommandNode):
    def __init__(self):
        super().__init__(None, lambda c: True, None, lambda s: [s.get_source()], False)
    
    def get_name(self):
        return ""
    
    def get_usage_text(self):
        return ""
    
    def parse(self, reader, context_builder):
        pass
    
    def list_suggestions(self, context, builder):
        return empty_suggestion()
    
    def is_valid_input(self, str_input):
        return False
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, RootCommandNode):
            return False
        
        return super.__eq__(obj)
    
    def create_builder(self):
        raise ValueError("Cannot convert root into a builder")
    
    def get_sorted_keys(self):
        return ""
    
    def get_examples(self):
        return []
    
    def __str__(self):
        return "<root>"

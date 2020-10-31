from .string_range import between


class ParsedArgument:
    def __init__(self, start, end, result):
        self.range = between(start, end)
        self.result = result
    
    def get_range(self):
        return self.range
    
    def get_result(self):
        return self.result
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, ParsedArgument):
            return False
        
        return self.range == obj.range and self.result == obj.result
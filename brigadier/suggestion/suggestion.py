import functools


@functools.total_ordering
class Suggestion:
    def __init__(self, str_range, text, tooltip=None):
        self.range = str_range
        self.text = text
        self.tooltip = tooltip
    
    def get_range(self):
        return self.range
    
    def get_text(self):
        return self.text
    
    def get_tooltip(self):
        return self.tooltip
    
    def apply(self, str_input):
        if self.range.get_start() == 0 and self.range.get_end() == len(str_input):
            return self.text
        
        result = ""
        if self.range.get_start() > 0:
            result += str_input[:self.range.get_start()]
        result += self.text
        if self.range.get_end() < len(str_input):
            result += str_input[self.range.get_end():]
        return result
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, Suggestion):
            return False
        
        return self.range == obj.range and self.text == obj.text and self.tooltip == obj.tooltip
    
    def __str__(self):
        return f"<Suggestion range={self.range}> text={self.text} tooltip={self.tooltip}>"
    
    def __lt__(self, obj):
        return self.text.lower() < obj.text.lower()
    
    #def lowercase_compare(self, obj):
    #    return self.text.lower() < obj.text.lower()
    
    def expand(self, command, str_range):
        if str_range == self.range:
            return self
        
        result = ""
        if str_range.get_start() < self.range.get_start():
            result += command[str_range.get_start():self.range.get_start()]
        
        result += self.text
        if str_range.get_end() > self.range.get_end():
            result += command[self.range.get_end():str_range.get_end()]
        
        return self.__init__(str_range, result, self.tooltip)

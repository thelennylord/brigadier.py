import functools

from .Suggestion import Suggestion


@functools.total_ordering
class IntegerSuggestion(Suggestion):
    def __init__(self, str_range, value, tooltip=None):
        super().__init__(str_range, str(value), tooltip)
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, IntegerSuggestion):
            return False
        
        return self.value == obj.value and self.get_range() == obj.get_range() and self.get_text() == obj.get_text() and self.get_tooltip() == obj.get_tooltip()
    
    def __str__(self):
        return f"<IntegerSuggestion value={self.get_value()} str_range={self.get_range()} text='{self.get_text()}' tooltip='{self.get_tooltip()}'>"

    def __lt__(self, obj):
        if isinstance(obj, IntegerSuggestion):
            if self.value < obj.value:
                return 1
            elif self.value > obj.value:
                return -1
            else:
                return 0
            
        return self.get_text() < obj.get_text()
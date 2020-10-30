import math

from brigadier.context.StringRange import StringRange, at


class Suggestions:
    
    def __init__(self, str_range, suggestions):
        self.range = str_range
        self.suggestions = suggestions
                   
    def get_range(self):
        return self.range

    def get_list(self):
        return self.suggestions

    def is_empty(self):
        return not self.suggestions

    def __eq__(self, obj):
        if self is obj:
            return True

        if not isinstance(obj, Suggestions):
            return False

        return self.range == obj.range and self.suggestions == obj.suggestions
    
    def __str__(self):
        return f"<Suggestions str_range={self.range} suggestions={self.suggestions}>"
    
    def merge(self, command, str_input):
        if not str_input:
            return EMPTY
        
        if len(str_input) == 1:
            return str_input[0]
        
        texts = []
        for suggestions in str_input:
            texts.append(*suggestions.get_list())
        
        return create_suggestion(command, texts)
    


EMPTY = Suggestions(at(0), [])

def create_suggestion(command, suggestions):
    if not suggestions:
        return EMPTY
    
    # TODO: check if it works with math.inf; if not, use 9223372036854775807 instead
    start = math.inf
    end = -math.inf
    for suggestion in suggestions:
        start = min(suggestion.get_range().get_start(), start)
        end = max(suggestion.get_range().get_end(), end)
    
    str_range = StringRange(start, end)
    texts = []
    for suggestion in suggestions:
        texts.append(suggestion.expand(command, str_range))

    sorted_sug = sorted(texts)
    return Suggestions(str_range, sorted_sug)

async def empty_suggestion():
    return EMPTY

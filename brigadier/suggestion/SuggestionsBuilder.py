from brigadier.context.StringRange import between

from .IntegerSuggestion import IntegerSuggestion
from .Suggestion import Suggestion
from .Suggestions import create_suggestion


class SuggestionsBuilder:

    def __init__(self, str_input, start):
        self.input = str_input
        self.start = start
        self.remaining = str_input[start:]
        self.result = []
    
    def get_input(self):
        return self.input
    
    def get_start(self):
        return self.start
    
    def get_remaining(self):
        return self.get_remaining
    
    def build(self):
        return create_suggestion(command=self.input, suggestions=self.result)
    
    async def build_async(self):
        return self.build()
    
    def suggest(self, text, tooltip):
        if isinstance(text, int):
            self.result.append(IntegerSuggestion(between(self.start, len(self.input)), text, tooltip))
            return self
        
        if text == self.remaining:
            return self

        self.result.append(Suggestion(between(self.start, len(self.input)), text, tooltip))
        return self
    
    def add(self, other):
        self.result.append(*other.result)
        return self
    
    def create_offset(self, start):
        return SuggestionsBuilder(self.input, start)
    
    def restart(self):
        return SuggestionsBuilder(self.input, self.start)

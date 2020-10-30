from .CommandSyntaxException import CommandSyntaxException


class SimpleCommandExceptionType:
    def __init__(self, message):
        self.message = message
    
    def create(self):
        return CommandSyntaxException(self, self.message)
    
    def create_with_context(self, reader):
        return CommandSyntaxException(self, self.message, reader.get_string(), reader.get_cursor())
    
    def __str__(self):
        return self.message.get_string()

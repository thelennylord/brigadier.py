from .command_syntax_exception import CommandSyntaxException


class DynamicCommandExceptionType:
    def __init__(self, function):
        self.function = function
    
    def create(self, *args):
        return CommandSyntaxException(self, self.function(*args))
    
    def create_with_context(self, reader, *args):
        return CommandSyntaxException(self, self.function(*args), reader.get_string(), reader.get_cursor())

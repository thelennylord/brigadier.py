import math

from brigadier.exceptions import BuiltInExceptions

EXAMPLES = ["0", "123", "-123"]

class IntegerArgumentType:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
        
    def get_integer(self, context, name):
        return context.get_argument(name, int)
    
    def get_minimum(self):
        return self.minimum
    
    def get_maximum(self):
        return self.maximum

    def __traceback__(self, tb):
        return self
    
    def parse(self, reader):
        start = reader.get_cursor()
        result = reader.read_int()

        if result < self.minimum:
            reader.set_cursor(start)
            raise BuiltInExceptions.integer_too_low().create_with_context(reader, result, self.minimum)
        
        if result > self.maximum:
            reader.set_cursor(start)
            raise BuiltInExceptions.integer_too_high().create_with_context(reader, result, self.maximum)

        return result
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, IntegerArgumentType):
            return False
        
        return self.maximum == obj.maximum and self.minimum == obj.minimum
    
    def __str__(self):
        if self.minimum == -math.inf and self.maximum == math.inf:
            return "integer()"
        elif self.maximum == math.inf:
            return f"integer({self.minimum})"
        else:
            return f"integer({self.minimum}, {self.maximum})"
    
    def __hash__(self):
        return 31 * self.minimum + self.maximum
    
    def get_examples(self):
        return EXAMPLES

def integer(minimum=-9223372036854775807, maximum=9223372036854775807):
    return IntegerArgumentType(minimum, maximum)

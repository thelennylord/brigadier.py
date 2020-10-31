import math

from brigadier.exceptions import BuiltInExceptions

EXAMPLES = ["0", "1.2", ".5", "-1", "-.5", "-1234.56"]

class FloatArgumentType:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum
    
    def get_float(self, context, name):
        return context.get_argument(name, float)
    
    def get_minimum(self):
        return self.minimum
    
    def get_maximum(self):
        return self.maximum
    
    def parse(self, reader):
        start = reader.get_cursor()
        result = reader.read_double()

        if result < self.minimum:
            reader.set_cursor(start)
            raise BuiltInExceptions.float_too_low().create_with_context(reader, result, self.minimum)
        
        if result > self.minimum:
            reader.set_cursor(start)
            raise BuiltInExceptions.float_too_high().create_with_context(reader, result, self.maximum)

        return result
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, FloatArgumentType):
            return False
        
        return self.maximum == obj.maximum and self.minimum == obj.minimum
    
    def __str__(self):
        if self.minimum == -math.inf and self.maximum == math.inf:
            return "float()"
        elif self.maximum == math.inf:
            return f"float({self.minimum})"
        else:
            return f"float({self.minimum}, {self.maximum})"
    
    def get_examples(self):
        return EXAMPLES

def float_type(minimum=-math.inf, maximum=math.inf):
    return FloatArgumentType(minimum, maximum)
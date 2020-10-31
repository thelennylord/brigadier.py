from .bool_argument_type import BoolArgumentType
from .integer_argument_type import IntegerArgumentType, integer
from .float_argument_type import FloatArgumentType, float_type
from .string_argument_type import StringArgumentType, word, string, greedy_string

boolean = BoolArgumentType()
integer = integer()
float_type = float_type()
word = word()
string = string()
greedy_string = greedy_string()

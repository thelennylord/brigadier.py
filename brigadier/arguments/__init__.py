from .BoolArgumentType import BoolArgumentType
from .IntegerArgumentType import IntegerArgumentType, integer
from .FloatArgumentType import FloatArgumentType, float_type
from .StringArgumentType import StringArgumentType, word, string, greedy_string

boolean = BoolArgumentType()
integer = integer()
float_type = float_type()
word = word()
string = string()
greedy_string = greedy_string()

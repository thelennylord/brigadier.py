import string
from brigadier.exceptions import BuiltInExceptions

class StringReader:
    SYNTAX_ESCAPE = "\\"
    SYNTAX_DOUBLE_QUOTE = '"'
    SYNTAX_SINGLE_QUOTE = "'"

    def __init__(self, obj):
        if isinstance(obj, str):
            self.string = obj
            self.cursor = 0
        elif isinstance(obj, StringReader):
            self.string = obj.string
            self.cursor = obj.cursor
            
    def get_string(self):
        return self.string
    
    def set_cursor(self, cursor):
        self.cursor = cursor
    
    def get_remaining_length(self):
        return len(self.string) - self.cursor
    
    def get_total_length(self):
        return len(self.string)

    def get_cursor(self):
        return self.cursor
    
    def get_read(self):
        return self.string[:self.cursor]
    
    def get_remaining(self):
        return self.string[self.cursor:]

    def can_read(self, length=1):
        return (self.cursor + length) <= len(self.string)
    
    def peek(self, offset=0):
        return self.string[self.cursor + offset]

    def read(self):
        result = self.string[self.cursor]
        self.cursor += 1
        return result
    
    def skip(self, count=1):
        self.cursor += count

    def is_allowed_number(self, char):
        return char >= '0' and char <= '9' or char == '.' or char == '-'
    
    def is_quoted_string_start(self, char):
        return char == self.SYNTAX_DOUBLE_QUOTE or char == self.SYNTAX_SINGLE_QUOTE
    
    def skip_whitespace(self):
        while self.can_read() and self.peek() in string.whitespace:
            self.skip()
    
    def read_int(self):
        start = self.cursor
        while self.can_read() and self.is_allowed_number(self.peek()):
            self.skip()
        
        number = self.string[start:self.cursor]
        if not number:
            raise BuiltInExceptions.reader_expected_int().create_with_context(self)
        
        try:
            return int(number)
        except ValueError:
            self.cursor = start
            raise BuiltInExceptions.reader_invalid_int().create_with_context(self, number)
        
    # def read_long(self):
    #     # TODO: verify long
    #     start = self.cursor
    #     while self.can_read() and self.is_allowed_number(self.peek()):
    #         self.skip()
        
    #     number = self.string[start:self.cursor]
    #     if not number:
    #         raise BuiltInExceptions.reader_expected_long().create_with_context(self)

    #     try:
    #         return int(number)
    #     except ValueError:
    #         self.cursor = start
    #         raise BuiltInExceptions.reader_invalid_long().create_with_context(self, number)

    # def read_double(self):
    #     # TODO: verify double
    #     start = self.cursor
    #     while self.can_read() and self.is_allowed_number(self.peek()):
    #         self.skip()
        
    #     number = self.string[start:self.cursor]
    #     if not number:
    #         raise BuiltInExceptions.reader_expected_double().create_with_context(self)
        
    #     try:
    #         return float(number)
    #     except ValueError:
    #         self.cursor = start
    #         raise BuiltInExceptions.reader_invalid_double().create_with_context(self, number)
    
    def read_float(self):
        start = self.cursor
        while self.can_read() and self.is_allowed_number(self.peek()):
            self.skip()
        
        number = self.string[start:self.cursor]
        if not number:
            raise BuiltInExceptions.reader_expected_float().create_with_context(self)
        
        try:
            return float(number)
        except ValueError:
            self.cursor = start
            raise BuiltInExceptions.reader_invalid_float().create_with_context(self, number)
    
    def read_unquoted_string(self):
        start = self.cursor
        while self.can_read() and is_allowed_in_unquoted_string(self.peek()):
            self.skip()
    
        return self.string[start:self.cursor]

    def read_quoted_string(self):
        if not self.can_read():
            return ""
        
        next_char = self.peek()
        if not self.is_quoted_string_start(next_char):
            raise BuiltInExceptions.reader_expected_start_of_quote().create_with_context(self)
        
        self.skip()
        return self.read_string_until(next_char)

    def read_string_until(self, terminator):
        result = ""
        escaped = False
        while self.can_read():
            char = self.read()
            if escaped:
                if char == terminator or char == self.SYNTAX_ESCAPE:
                    result += char
                else:
                    self.set_cursor(self.get_cursor() - 1)
                    raise BuiltInExceptions.reader_invalid_escape().create_with_context(self, str(char))
            elif char == self.SYNTAX_ESCAPE:
                escaped = True
            elif char == terminator:
                return result
            else:
                result += char
        
        raise BuiltInExceptions.reader_expected_end_of_quote().create_with_context(self)
    
    def read_string(self):
        if not self.can_read():
            return ""
        
        next_char = self.peek()
        if self.is_quoted_string_start(next_char):
            self.skip()
            return self.read_string_until(next_char)
        
        return self.read_unquoted_string()
    
    def read_boolean(self):
        start = self.cursor
        value = self.read_unquoted_string()

        if not value:
            raise BuiltInExceptions.reader_expected_bool().create_with_context(self)

        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            self.cursor = start
            raise BuiltInExceptions.reader_invalid_bool().create_with_context(self, value)
    
    def expect(self, char):
        if not self.can_read() or self.peek() != char:
            raise BuiltInExceptions.reader_expected_symbol().create_with_context(self, str(char))
            
        self.skip()

def is_allowed_in_unquoted_string(char):
    return char.isalnum() or char == '_' or char == '-' or char == '.' or char == '+'
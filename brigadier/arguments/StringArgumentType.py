from brigadier.StringReader import is_allowed_in_unquoted_string


SINGLE_WORD = "words_with_underscores",
QUOTABLE_PHRASE = "\"quoted phrase\"",
GREEDY_PHRASE = "words with spaces"

class StringArgumentType:
    def __init__(self, str_type):
        self.type = str_type
    
    def get_string(self, context, name):
        return context.get_argument(name, str)
    
    def get_type(self):
        return self.type
    
    def parse(self, reader):
        if self.type == GREEDY_PHRASE:
            text = reader.get_remaining()
            reader.set_cursor(reader.get_total_length())
            return text
        elif self.type == SINGLE_WORD:
            return reader.read_unquoted_string()
        else:
            return reader.read_string()
        
    def __str__(self):
        return "string()"
    
    def get_examples(self):
        pass
    
    def escape_if_required(self, str_input):
        for char in str_input:
            if not is_allowed_in_unquoted_string(char):
                return self.escape(str_input)
        return str_input
    
    def escape(self, str_input):
        result = '"'
        for char in str_input:
            if char == "\\" or char == '"':
                result += "\\"
            result += char
        result += '"'
        return result

def word():
    return StringArgumentType(SINGLE_WORD)

def string():
    return StringArgumentType(QUOTABLE_PHRASE)

def greedy_string():
    return StringArgumentType(GREEDY_PHRASE)
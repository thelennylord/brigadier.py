from brigadier.StringReader import StringReader

class ParseResult:
    def __init__(self, context, reader=StringReader(""), exceptions={}):
        self.context = context
        self.reader = reader
        self.exceptions = exceptions
    
    def get_context(self):
        return self.context

    def get_reader(self):
        return self.reader
    
    def get_exceptions(self):
        return self.exceptions
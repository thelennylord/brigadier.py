class CommandSyntaxException(Exception):
    CONTEXT_AMOUNT = 50

    def __init__(self, exc_type, message, str_input=None, cursor=-1):
        super().__init__(message)
        self.type = exc_type
        self.message = message
        self.input = str_input
        self.cursor = cursor
    
    def get_message(self):
        message = self.message.get_string()
        context = self.get_context()
        if context is not None:
            message += f" at position {self.cursor}: {context}"
        return message
    
    def get_raw_message(self):
        return self.message
    
    def get_context(self):
        if self.input is None or self.cursor < 0:
            return None
        
        builder = ""
        cursor = min(len(self.input), self.cursor)
        if cursor > self.CONTEXT_AMOUNT:
            builder += "..."

        builder += self.input[max(0, self.cursor - self.CONTEXT_AMOUNT):(cursor + 1)]
        builder += "<--[HERE]"

        return builder
    
    def get_type(self):
        return self.type
    
    def get_input(self):
        return self.input
    
    def get_cursor(self):
        return self.cursor
        


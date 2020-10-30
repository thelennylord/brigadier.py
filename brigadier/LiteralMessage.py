class LiteralMessage:
    def __init__(self, string):
        self.string = string
    
    def get_string(self):
        return self.string
    
    def __str__(self):
        return self.string
class StringRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
   
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get(self, string):
        return string[self.start:self.end]

    def is_empty(self):
        return self.start == self.end
    
    def __len__(self):
        return self.end - self.start
    
    def __eq__(self, obj):
        if not isinstance(obj, StringRange):
            return False
        
        return self.start == obj.start and self.end == obj.end
    
    def __str__(self):
        return f"<StringRange start={self.start} end={self.end}>"

def at(pos):
    return StringRange(pos, pos)

def between(start, end):
    return StringRange(start, end)

def encompassing(a, b):
    return StringRange(min(a.get_start(), b.get_start()), max(a.get_end(), b.get_end()))
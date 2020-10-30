class ParsedCommandNode:
    def __init__(self, node, str_range):
        self.node = node
        self.range = str_range
    
    def get_node(self):
        return self.node
    
    def get_range(self):
        return self.range
    
    def __str__(self):
        return f"{self.node}@{self.range}"
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, ParsedCommandNode):
            return False
            
        return self.node == obj.node and self.range == obj.range        
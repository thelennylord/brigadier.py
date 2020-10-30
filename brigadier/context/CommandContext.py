class CommandContext:
    def __init__(self, source, str_input, arguments, command, root_node, nodes, str_range, child, modifier, forks):
        self.source = source
        self.input = str_input
        self.arguments = arguments
        self.command = command
        self.root_node = root_node
        self.nodes = nodes
        self.range = str_range
        self.child = child
        self.modifier = modifier
        self.forks = forks
    
    def copy_for(self, source):
        if self.source == source:
            return self
        return CommandContext(source, self.input, self.arguments, self.command, self.root_node, self.nodes, self.range, self.child, self.modifier, self.forks)
    
    def get_child(self):
        return self.child
    
    def get_last_child(self):
        result = self
        while result.get_child() is not None:
            result = result.get_child()
        return result

    def get_command(self):
        return self.command
    
    def get_source(self):
        return self.source
    
    def get_argument(self, name, clazz=None):
        try:
            argument = self.arguments[name]
            result = argument.get_result()
            if clazz is None:
                return result
            else:
                return clazz(result)
        except KeyError:
            raise ValueError(f"No such argument '{name}' exists on this command")
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, CommandContext):
            return False
        
        if self.arguments != obj.arguments:
            return False
        
        if self.root_node != obj.root_node:
            return False
        
        if len(self.nodes) != len(obj.nodes) or self.nodes != obj.nodes:
            return False
        
        if (self.command != obj.command if self.command is not None else obj.command is not None):
            return False

        if self.source != obj.source:
            return False

        if (self.child != obj.child if self.child is not None else obj.child is  None):
            return False

        return True
    
    def __hash__(self):
        result = hash(self.source)
        result = 31 * result + hash(self.arguments)
        result = 31 * result + hash(self.command) if self.command is not None else 0
        result = 31 * result + hash(self.root_node)
        result = 31 * result + hash(self.nodes)
        result = 31 * result + hash(self.child) if self.child is not None else 0
        return result

    def get_redirect_modifier(self):
        return self.modifier

    def get_range(self):
        return self.range

    def get_root_node(self):
        return self.root_node

    def get_nodes(self):
        return self.nodes

    def has_nodes(self):
        return self.nodes

    def is_forked(self):
        return self.forks 
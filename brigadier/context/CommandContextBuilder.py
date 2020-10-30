from .CommandContext import CommandContext
from .ParsedCommandNode import ParsedCommandNode
from .StringRange import at, encompassing
from .SuggestionContext import SuggestionContext


class CommandContextBuilder:

    def __init__(self, dispatcher, source, root_node, start):
        self.dispatcher = dispatcher
        self.source = source
        self.root_node = root_node
        self.range = at(start)
        
        self.arguments = {}
        self.nodes = []
        self.command = None
        self.child = None
        self.modifier = None
        self.forks = None
    
    def with_source(self, source):
        self.source = source
        return self
    
    def get_source(self):
        return self.source
    
    def get_root_node(self):
        return self.root_node
    
    def with_argument(self, name, arguments):
        self.arguments[name] = arguments
        return self
    
    def get_arguments(self):
        return self.arguments

    def with_command(self, command):
        self.command = command
        return self
    
    def with_node(self, node, str_range):
        self.nodes.append(ParsedCommandNode(node, str_range))
        self.range = encompassing(self.range, str_range)
        self.modifier = node.get_redirect_modifier()
        self.forks = node.is_fork()
        return self
    
    def copy(self):
        copy = CommandContextBuilder(self.dispatcher, self.source, self.root_node, self.range.get_start())
        copy.command = self.command
        copy.arguments = self.arguments
        copy.nodes = self.nodes
        copy.child = self.child
        copy.range = self.range
        copy.forks = self.forks
        return copy
    
    def with_child(self, child):
        self.child = child
        return self
    
    def get_child(self):
        return self.child
    
    def get_last_child(self):
        result = self
        while self.get_child() is not None:
            result = self.get_child()
        return result
    
    def get_command(self):
        return self.command
    
    def get_nodes(self):
        return self.nodes
    
    def build(self, str_input):
        return CommandContext(self.source, str_input, self.arguments, self.command, self.root_node, self.nodes, self.range, None if self.child is None else self.child.build(str_input), self.modifier, self.forks)
    
    def get_dispatcher(self):
        return self.dispatcher
    
    def get_range(self):
        return self.range
    
    def find_suggestion_context(self, cursor):
        if self.range.get_start() <= cursor:
            if self.range.get_end() < cursor:
                if self.child is not None:
                    return self.child.find_suggestion_context(cursor)
                elif self.nodes:
                    last = self.nodes[-1]
                    return SuggestionContext(last.get_node(), last.get_range().get_end() + 1)
                else:
                    return SuggestionContext(self.root_node, self.range.get_start())
            else:
                prev = self.root_node
                for node in self.nodes:
                    node_range = node.get_range()
                    if node_range.get_start() <= cursor and cursor <= node_range.get_end():
                        return SuggestionContext(prev, node_range.get_start())
                    prev = node.get_node()
                if prev is None:
                    raise ValueError("Can't find node before cursor")
                return SuggestionContext(prev, self.range.get_start())
        raise ValueError("Can't find node before cursor")

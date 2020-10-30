import functools


@functools.total_ordering
class CommandNode:
    def __init__(self, command, requirement, redirect, modifier, forks):
        self.command = command
        self.requirement = (lambda c: True)
        self.redirect = redirect
        self.modifier = modifier
        self.forks = forks

        # dicts in Python 3.7 are insertion ordered
        self.children = {}
        self.literals = {}
        self.arguments = {}
    
    def get_command(self):
        return self.command
    
    def get_children(self):
        return self.children.values()
    
    def get_child(self, name):
        return self.children[name]

    def get_redirect(self):
        return self.redirect
    
    def get_redirect_modifier(self):
        return self.modifier
    
    def can_use(self, source):
        return self.requirement(source)
    
    def add_child(self, node):
        from brigadier.tree import (ArgumentCommandNode, LiteralCommandNode,
                                    RootCommandNode)
        
        if isinstance(node, RootCommandNode):
            raise ValueError("Cannot add a RootCommandNode as a child to any other CommandNode")
        
        try:
            child = self.children[node.get_name()]
            if node.get_command() is not None:
                child.command = node.get_command()
            
            for grandchild in node.get_children():
                child.add_child(grandchild)
        except KeyError:
            self.children[node.get_name()] = node
            if isinstance(node, LiteralCommandNode):
                self.literals[node.get_name()] = node
            elif isinstance(node, ArgumentCommandNode):
                self.arguments[node.get_name()] = node
        self.children = dict(sorted(self.children.items(), key=lambda item: item[1]))
    
    def find_ambiguities(self, consumer):
        matches = []
        for child in self.children.values():
            for sibling in self.children.values():
                if child == sibling:
                    continue
            
                for str_input in child.get_examples():
                    if sibling.is_valid_input(str_input):
                        matches.append(str_input)
                
                if matches:
                    consumer.ambiguous(self, child, sibling, matches)
                    matches = []
            
            child.find_ambiguities(consumer)
    
    def is_valid_input(self, str_input):
        raise NotImplementedError
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, CommandNode):
            return False
        
        if self.children != obj.children:
            return False
        
        if (self.command != obj.command if self.command is not None else obj.command is not None):
            return False
        
        return True
    
    def __hash__(self):
        return 31 * hash(self.children) + (hash(self.command) if self.command is not None else 0)
    
    def get_requirement(self):
        return self.requirement
    
    def get_name(self):
        raise NotImplementedError
    
    def get_usage_text(self):
        raise NotImplementedError
    
    def parse(self, reader, context_builder):
        raise NotImplementedError
    
    def list_suggestions(self, context, builder):
        raise NotImplementedError
    
    def create_builder(self):
        raise NotImplementedError
    
    def get_sorted_keys(self):
        raise NotImplementedError

    def get_relevant_nodes(self, str_input):
        if self.literals:
            cursor = str_input.get_cursor()
            while str_input.can_read() and str_input.peek() != ' ':
                str_input.skip()
            text = str_input.get_string()[cursor:str_input.get_cursor()]
            str_input.set_cursor(cursor)
            if text in self.literals:
                return [self.literals[text]]
            else:
                return self.arguments.values()
        else:
            return self.arguments.values()
    
    def __lt__(self, obj):
        from brigadier.tree.LiteralCommandNode import LiteralCommandNode

        if isinstance(self, LiteralCommandNode) == isinstance(obj, LiteralCommandNode):
            return self.get_sorted_keys() < obj.get_sorted_keys()
        
        return 1 if isinstance(obj, LiteralCommandNode) else -1
    
    def is_fork(self):
        return self.forks
    
    def get_examples(self):
        raise NotImplementedError

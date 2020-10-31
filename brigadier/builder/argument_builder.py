from brigadier.tree.root_command_node import RootCommandNode


class ArgumentBuilder:
    def __init__(self):
        self.arguments = RootCommandNode()
        self.command = None
        self.requirement = None
        self.target = None
        self.modifier = None
        self.forks = None
    
    def get_self(self):
        raise NotImplementedError
    
    def then(self, argument):
        if self.target is not None:
            raise ValueError("Cannot add children to a redirected node")
        
        if isinstance(argument, ArgumentBuilder):
            self.arguments.add_child(argument.build())
        else:
            self.arguments.add_child(argument)
        
        return self.get_self()

    def get_arguments(self):
        return self.arguments.get_children()
    
    def executes(self, command):
        self.command = command
        return self.get_self()
    
    def get_command(self):
        return self.command

    def requires(self, requirement):
        self.requirement = requirement
        return self.get_self()

    def get_requirement(self):
        return self.get_requirement

    def redirect(self, target, modifier=None):
        if modifier is None:
            return self.forward(target, None, False)
        else:
            return self.forward(target, lambda o: [modifier(o)], False)
    
    def fork(self, target, modifier):
        return self.forward(target, modifier, True)
    
    def forward(self, target, modifier, fork):
        if self.arguments.get_children():
            raise ValueError("Cannot forward a node with children")
        
        self.target = target
        self.modifier = modifier
        self.forks = fork
        return self.get_self()
    
    def get_redirect(self):
        return self.target
    
    def get_redirect_modifier(self):
        return self.modifier
    
    def is_fork(self):
        return self.forks
    
    def build(self):
        raise NotImplementedError

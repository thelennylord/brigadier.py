from brigadier import StringReader
from brigadier.context import ParsedArgument
from brigadier.exceptions import CommandSyntaxException

from .CommandNode import CommandNode


class ArgumentCommandNode(CommandNode):
    USAGE_ARGUMENT_OPEN = "<"
    USAGE_ARGUMENT_CLOSE = ">"

    def __init__(self, name, arg_type, command, requirement, redirect, modifier, forks, custom_suggestions):
        super().__init__(command, requirement, redirect, modifier, forks)
        self.name = name
        self.type = arg_type
        self.custom_suggestions = custom_suggestions
    
    def get_type(self):
        return self.type
    
    def get_name(self):
        return self.name
    
    def get_usage_text(self):
        return self.USAGE_ARGUMENT_OPEN + self.name + self.USAGE_ARGUMENT_CLOSE
    
    def get_custom_suggestions(self):
        return self.custom_suggestions
    
    def parse(self, reader, context_builder):
        start = reader.get_cursor()
        result = self.type.parse(reader)
        parsed = ParsedArgument(start, reader.get_cursor(), result)
        
        context_builder.with_argument(self.name, parsed)
        context_builder.with_node(self, parsed.get_range())
    
    async def list_suggestions(self, context, builder):
        if self.custom_suggestions is None:
            return self.type.list_suggestions(context, builder)
        else:
            return self.custom_suggestions.get_suggestions(context, builder)
    
    def create_builder(self):
        from brigadier.builder import RequiredArgumentBuilder

        builder = RequiredArgumentBuilder(self.name, self.type)
        builder.requires(self.get_requirement())
        builder.forward(self.get_redirect(), self.get_redirect_modifier(), self.is_fork())
        builder.suggests(self.custom_suggestions)
        
        if self.get_command() is not None:
            builder.executes(self.get_command())
        return builder

    def is_valid_input(self, str_input):
        try:
            reader = StringReader(str_input)
            self.type.parse(reader)
            return not reader.can_read() or reader.peek() == ' '
        # TODO: check if this works
        except CommandSyntaxException:
            return False
    
    def __eq__(self, obj):
        if self is obj:
            return True
        if not isinstance(obj, ArgumentCommandNode):
            return False
        if self.name != obj.name:
            return False
        if self.type != obj.type:
            return False
        return super.__eq__(obj)

    def get_sorted_keys(self):
        return self.name
    
    def get_examples(self):
        return self.type.get_examples()
    
    def __str__(self):
        return f"<argument {self.name}:{self.type}>"
    
    def __hash__(self):
        result = hash(self.name)
        result = 31 * result + hash(self.type)
        return result

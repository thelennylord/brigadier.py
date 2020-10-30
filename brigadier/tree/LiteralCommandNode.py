from brigadier import StringReader
from brigadier.builder import literal
from brigadier.context.StringRange import between
from brigadier.exceptions import BuiltInExceptions
from brigadier.suggestion import empty_suggestion
from brigadier.tree import CommandNode


class LiteralCommandNode(CommandNode):
    def __init__(self, literal, command, requirement, redirect, modifier, forks):
        super().__init__(command, requirement, redirect, modifier, forks)
        self.literal = literal
    
    def get_literal(self):
        return self.literal
    
    def get_name(self):
        return self.literal
    
    def parse(self, reader, context_builder):
        start = reader.get_cursor()
        end = self.__parse(reader)
        if end > -1:
            context_builder.with_node(self, between(start, end))
            return

        raise BuiltInExceptions.literal_incorrect().create_with_context(reader, self.literal)

    def __parse(self, reader):
        start = reader.get_cursor()
        if reader.can_read(len(self.literal)):
            end = start + len(self.literal)
            if reader.get_string()[start:end] == self.literal:
                reader.set_cursor(end)
                if not reader.can_read() or reader.peek() == " ":
                    return end
                else:
                    reader.set_cursor(start)
        return -1
    
    async def list_suggestions(self, context, builder):
        if self.literal.lower().startswith(builder.get_remaining().lower()):
            return await builder.suggest(self.literal).build_async()
        else:
            return empty_suggestion()

    def is_valid_input(self, str_input):
        return self.__parse(StringReader(str_input)) > -1
    
    def __eq__(self, obj):
        if self is obj:
            return True
        
        if not isinstance(obj, LiteralCommandNode):
            return False
        
        if self.literal != obj.literal:
            return False

        return super.__eq__(obj)
    
    def __hash__(self):
        result = hash(self.literal)
        result = 31 * result + super().__hash__()
        return result
    
    def create_builder(self):
        builder = literal(self.literal)
        builder.requires(self.get_requirement())
        builder.forward(self.get_redirect(), self.get_redirect_modifier(), self.is_fork())

        if self.get_command() is not None:
            builder.executes(self.get_command())
        
        return builder
    
    def get_sorted_keys(self):
        return self.literal
    
    def get_examples(self):
        return [self.literal]
    
    def __str__(self):
        return f"<literal {self.literal}>"
    
    def get_usage_text(self):
        return self.literal

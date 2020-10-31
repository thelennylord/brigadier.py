EXAMPLES = ["true", "false"]

class BoolArgumentType:    
    def get_bool(self, context, name):
        return context.get_argument(name, bool)

    def parse(self, reader):
        return reader.read_boolean()
    
    def list_suggestions(self, context, builder):
        if "true".startswith(builder.get_remaining().lower()):
            builder.suggest("true")
        
        if "false".startswith(builder.get_remaining().lower()):
            builder.suggest("false")
        
        return builder.build_async()
    
    def get_examples(self):
        return EXAMPLES
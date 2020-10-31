import functools

from brigadier.context import CommandContextBuilder
from brigadier.exceptions import BuiltInExceptions, CommandSyntaxException
from brigadier.suggestion import Suggestions, SuggestionsBuilder, empty_suggestion
from brigadier.tree import RootCommandNode

from .parse_result import ParseResult
from .result_consumer import ResultConsumer
from .string_reader import StringReader

ARGUMENT_SEPARATOR = " "
ARGUMENT_SEPARATOR_CHAR = " "
USAGE_OPTIONAL_OPEN = "["
USAGE_OPTIONAL_CLOSE = "]"
USAGE_REQUIRED_OPEN  = "("
USAGE_REQUIRED_CLOSE  = ")"
USAGE_OR = "|"

class CommandDispatcher:
    def __init__(self, root=RootCommandNode()):
        self.root = root
        self.consumer = ResultConsumer()

    def register(self, command):
        build = command.build()
        self.root.add_child(build)
        return build
    
    def set_consumer(self, consumer):
        self.consumer = consumer
    
    def execute(self, str_input, source={}):
        if isinstance(str_input, str):
            str_input = StringReader(str_input)
        
        # TODO: check if works
        parse = self.parse(str_input, source)
        return self.execute_preparsed(parse)

    def execute_preparsed(self, parse):

        if parse.get_reader().can_read():
            if len(parse.get_exceptions()) == 1:
                raise list(parse.get_exceptions().values())[0]
            elif not parse.get_context().get_range():
                raise BuiltInExceptions.dispatcher_unknown_command().create_with_context(parse.get_reader())
            else:
                raise BuiltInExceptions.dispatcher_unknown_argument().create_with_context(parse.get_reader())
        
        result = 0
        successful_forks = 0
        forked = False
        found_command = False
        command = parse.get_reader().get_string()
        original = parse.get_context().build(command)
        contexts = [original]
        _next = None

        while contexts is not None:
            for context in contexts:
                child = context.get_child()
                if child is not None:
                    forked |= context.is_forked()
                    if child.has_nodes():
                        found_command = True
                        modifier = context.get_redirect_modifier()
                        if modifier is None:
                            if _next is None:
                                _next = []
                            _next.append(child.copy_for(context.get_source()))
                        else:
                            try:
                                results = modifier(context)
                                if results:
                                    if _next is None:
                                        _next = []
                                    for source in results:
                                        _next.append(child.copy_for(source))
                            except CommandSyntaxException as e:
                                self.consumer.on_command_complete(context, False, 0)
                                if not forked:
                                    raise e
                elif context.get_command() is not None:
                    found_command = True
                    try:
                        value = context.get_command()(context)                            
                        result += value if value else 1
                        self.consumer.on_command_complete(context, True, value)
                        successful_forks += 1
                    except CommandSyntaxException as e:
                        self.consumer.on_command_complete(context, False, 0)
                        if not forked:
                            raise e
            
            contexts = _next
            _next = None
        
        if not found_command:
            self.consumer.on_command_complete(original, False, 0)
            raise BuiltInExceptions.dispatcher_unknown_command().create_with_context(parse.get_reader())
        
        return successful_forks if forked else result

    def parse(self, command, source):
        if isinstance(command, str):
            command = StringReader(command)

        context = CommandContextBuilder(self, source, self.root, command.get_cursor())
        return self.parse_nodes(self.root, command, context)
    
    def parse_nodes(self, node, original_reader, context_so_far):
        source = context_so_far.get_source()
        errors = None
        potentials = None
        cursor = original_reader.get_cursor()

        for child in node.get_relevant_nodes(original_reader):
            if not child.can_use(source):
                continue
            
            context = context_so_far.copy()
            reader = StringReader(original_reader)
            try:
                try:
                    child.parse(reader, context)
                # TODO: check if this one's appropriate
                except RuntimeError as e:
                    raise BuiltInExceptions.dispatcher_parse_expection().create_with_context(reader, e)
                
                if reader.can_read():
                    if reader.peek() != ARGUMENT_SEPARATOR_CHAR:
                        raise BuiltInExceptions.dispatcher_expected_argument_separator().create_with_context(reader)
            except CommandSyntaxException as e:
                if errors is None:
                    errors = {}
                errors[child] = e
                reader.set_cursor(cursor)
                continue
            
            context.with_command(child.get_command())
            if reader.can_read(2 if child.get_redirect() is None else 1):
                reader.skip()
                if child.get_redirect() is not None:
                    child_context = CommandContextBuilder(self, source, child.get_redirect(), reader.get_cursor())
                    parse = self.parse_nodes(child.get_redirect(), reader, child_context)
                    context.with_child(parse.get_context())
                    return ParseResult(context, parse.get_reader(), parse.get_exceptions())
                else:
                    parse = self.parse_nodes(child, reader, context)
                    if potentials is None:
                        potentials = []
                    potentials.append(parse)
            else:
                if potentials is None:
                    potentials = []
                potentials.append(ParseResult(context, reader, {}))

        if potentials:
            potentials.sort(key=functools.cmp_to_key(potentials_cmp))
            return potentials[0]
        return ParseResult(context_so_far, original_reader, {} if errors is None else errors)
            
    def get_all_usage(self, node, source, restricted):
        result = []
        return self.__get_all_usage(node, source, result, "", restricted)
        #return result
    
    def __get_all_usage(self, node, source, result, prefix, restricted):
        if restricted and not node.can_use(source):
            return
        
        if node.get_command() is not None:
            result.append(prefix)
        
        if node.get_redirect() is not None:
            redirect = "..." if node.get_redirect() == self.root else f"-> {node.get_redirect().get_usage_text()}"
            result.append(node.get_usage_text() + ARGUMENT_SEPARATOR + redirect if not prefix else prefix + ARGUMENT_SEPARATOR + redirect)
        elif node.get_children():
            for child in node.get_children():
                self.__get_all_usage(child, source, result, child.get_usage_text() if not prefix else prefix + ARGUMENT_SEPARATOR + child.get_usage_text(), restricted)

        return result
    
    def get_smart_usage(self, node, source, optional, deep):
        if not node.can_use(source):
            return None
        
        this = USAGE_OPTIONAL_OPEN + node.get_usage_text() + USAGE_OPTIONAL_CLOSE if optional else node.get_usage_text()
        child_optional = node.get_command() is not None
        open_str = USAGE_OPTIONAL_OPEN if child_optional else USAGE_REQUIRED_OPEN
        close_str = USAGE_OPTIONAL_CLOSE if child_optional else USAGE_OPTIONAL_CLOSE

        if not deep:
            if node.get_redirect() is not None:
                redirect = "..." if node.get_redirect() == self.root else f"-> {node.get_redirect().get_usage_text()}"
                return this + ARGUMENT_SEPARATOR + self.redirect
            else:
                children = list(filter(lambda c: c.can_use(source), node.get_children()))
                if len(children) == 1:
                        usage = self.__get_smart_usage(children[0], source, child_optional, child_optional)
                        if usage is not None:
                            return this + ARGUMENT_SEPARATOR + usage
                elif len(children) > 1:
                    child_usage = set()
                    for child in children:
                        usage = self.__get_smart_usage(child, source, child_optional, True)
                        if usage is not None:
                            child_usage.add(usage)
                    if len(child_usage) == 1:
                        usage = next(iter(child_usage))
                        return this + ARGUMENT_SEPARATOR + (USAGE_OPTIONAL_OPEN + usage + USAGE_OPTIONAL_CLOSE if child_optional else usage)
                    elif len(child_usage) > 1:
                        builder = open_str
                        count = 0
                        for child in children:
                            if count > 0:
                                builder += USAGE_OR
                            builder += child.get_usage_text
                            count += 1
                        if count > 0:
                            builder += close_str
                            return this + ARGUMENT_SEPARATOR + builder
        return this
    
    async def get_completion_suggestions(self, parse, cursor=None):
        if cursor is None:
            cursor = parse.get_reader().get_total_length()
        
        context = parse.get_context()
        node_before_cursor = context.find_suggestion_context(cursor)
        parent = node_before_cursor.parent
        start = min(node_before_cursor.start_pos, cursor)

        full_input = parse.get_reader().get_string()
        truncated_input = full_input[:cursor]
        futures = []
        for node in parent.get_children():
            future = empty_suggestion()
            try:
                future = node.list_suggestions(context.build(truncated_input), SuggestionsBuilder(truncated_input, start))
            except CommandSyntaxException:
                pass
            futures.append(future)
        
        return Suggestions.merge(full_input, futures)
    
    def get_root(self):
        return self.root
    
    def get_path(self, target):
        nodes = []
        self.add_paths(self.root, nodes, [])

        for _list in nodes:
            if _list[-1] == target:
                result = []
                for node in _list:
                    if node != self.root:
                        result.append(node.get_name())
                return result
        
        return []

    def find_node(self, path):
        node = self.root
        for name in path:
            node = node.get_child(name)
            if node is None:
                return None
        return node
    
    def find_ambiguities(self, consumer):
        self.root.find_ambiguities(consumer)
    
    def add_paths(self, node, result, parents):
        current = []
        current.append(node)
        result.append(current)
        for child in node.get_children():
            self.add_paths(child, result, current)

def potentials_cmp(a, b):
    if (not a.get_reader().can_read()) and b.get_reader().can_read():
        return -1
    if a.get_reader().can_read() and not b.get_reader().can_read():
        return 1
    if (not a.get_exceptions()) and b.get_exceptions():
        return -1
    if a.get_exceptions() and not b.get_exceptions():
        return 1
    return 0

from brigadier import CommandDispatcher, StringReader
from brigadier.arguments import greedy_string, integer, string, word
from brigadier.builder import argument, literal
from brigadier.context import CommandContext
from brigadier.exceptions import BuiltInExceptions, CommandSyntaxException


def command(ctx):
    assert isinstance(ctx, CommandContext)
    return 42

def subcommand(ctx):
    assert isinstance(ctx, CommandContext)
    return 100

def input_with_offset(input, offset):
    result = StringReader(input)
    result.set_cursor(offset)
    return result

def test_create_and_execute_command():
    subject = CommandDispatcher()
    subject.register(literal("foo").executes(command))
    assert subject.execute("foo", {}) == 42

def test_create_and_execute_offset_command():
    subject = CommandDispatcher()
    subject.register(literal("foo").executes(command))
    assert subject.execute(input_with_offset("/foo", 1), {}) == 42

def test_create_and_merge_commands():
    subject = CommandDispatcher()
    subject.register(literal("base").then(literal("foo").executes(command)))
    subject.register(literal("base").then(literal("bar").executes(command)))
    assert subject.execute("base foo", {}) == 42
    assert subject.execute("base bar", {}) == 42

def test_execute_unknown_command():
    subject = CommandDispatcher()
    subject.register(literal("bar"))
    subject.register(literal("baz"))
    
    try:
        subject.execute("foo", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_command()
        assert error.get_cursor() == 0

def test_execute_impermissible_command():
    subject = CommandDispatcher()
    subject.register(literal("foo").requires(lambda _: False))
    
    try:
        subject.execute("foo", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_command()
        assert error.get_cursor() == 0

def test_execute_empty_command():
    subject = CommandDispatcher()
    subject.register(literal(""))
        
    try:
        subject.execute("", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_command()
        assert error.get_cursor() == 0

def test_execute_unknown_subcommand():
    subject = CommandDispatcher()
    subject.register(literal("foo").executes(command))

    try:
        subject.execute("foo bar", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_argument()
        assert error.get_cursor() == 4

def test_execute_incorrect_literal():
    subject = CommandDispatcher()
    subject.register(literal("foo").executes(command).then(literal("bar")))

    try:
        subject.execute("foo baz", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_argument()
        assert error.get_cursor() == 4

def test_execute_ambiguous_incorrect_argument():
    subject = CommandDispatcher()
    subject.register(
        literal("foo").executes(command).then(literal("bar")).then(literal("baz"))
    )

    try:
        subject.execute("foo unknown", {})
    except CommandSyntaxException as error:
        assert error.get_type() == BuiltInExceptions.dispatcher_unknown_argument()
        assert error.get_cursor() == 4

def test_execute_subcommand():
    subject = CommandDispatcher()
    subject.register(
        literal("foo").then(
            literal("a")
        ).then(
            literal("=").executes(subcommand)
        ).then(
            literal("c")
        ).executes(command)
    )

    assert subject.execute("foo =", {}) == 100

def test_parse_incomplete_literal():
    subject = CommandDispatcher()
    subject.register(literal("foo").then(literal("bar").executes(command)))
    parse = subject.parse("foo ", {})
    assert parse.get_reader().get_remaining() == " "
    assert len(parse.get_context().get_nodes()) == 1

def test_parse_incomplete_argument():
    subject = CommandDispatcher()
    subject.register(
        literal("foo").then(
            argument("bar", integer).executes(command)
        )
    )
    parse = subject.parse("foo ", {})
    assert parse.get_reader().get_remaining() == " "
    assert len(parse.get_context().get_nodes()) == 1

def test_execute_ambiguous_parent_subcommand():
    subject = CommandDispatcher()
    subject.register(
        literal("test").then(
            argument("incorrect", integer).executes(command)
        ).then(
            argument("right", integer).then(
                argument("sub", integer).executes(subcommand)
            )
        )
    )

    assert subject.execute("test 1 2", {}) == 100

def test_execute_ambiguous_parent_subcommand_via_redirect():
    subject = CommandDispatcher()
    real = subject.register(
        literal("test").then(
            argument("incorrect", integer).executes(command)
        ).then(
            argument("right", integer).then(
                argument("sub", integer).executes(subcommand)
            )
        )
    )
    subject.register(literal("redirect").redirect(real))
    assert subject.execute("redirect 1 2", {}) == 100

def test_execute_redirected_multiple_times():
    subject = CommandDispatcher()
    concrete_node = subject.register(literal("actual").executes(command))
    redirect_node = subject.register(literal("redirected").redirect(subject.get_root()))
    cmd_input = "redirected redirected actual"

    parse = subject.parse(cmd_input, {})
    assert parse.get_context().get_range().get(cmd_input) == "redirected"
    assert len(parse.get_context().get_nodes()) == 1
    assert parse.get_context().get_root_node() == subject.get_root()
    assert parse.get_context().get_nodes()[0].get_range() == parse.get_context().get_range()
    assert parse.get_context().get_nodes()[0].get_node() == redirect_node

    # Continue from
    # https://github.com/Mojang/brigadier/blob/master/src/test/java/com/mojang/brigadier/CommandDispatcherTest.java#L274

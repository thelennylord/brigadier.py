# brigadier.py
Implementation of [Mojang/brigadier](https://github.com/Mojang/brigadier) in Python.

## Installing
------------
**Requires Python 3.7 or higher**

## Examples
-----------

### Registering a simple command
```py
from brigadier import CommandDispatcher
from brigadier.builder import literal, argument
from brigadier.arguments import integer

def pow2_command(ctx):
    number = ctx.get_argument("number")
    return pow(number, 2)

def pow_command(ctx):
    number = ctx.get_argument("number")
    power = ctx.get_argument("power")
    return pow(number, power)

# Register the command
dispatcher = CommandDispatcher()
dispatcher.register(
    literal("pow2").then(
        argument("number", integer).executes(power_command)
    )
)

dispatcher.register(
    literal("pow").then(
        argument("number", integer).then(
            argument("power", integer).executes(pow_command)
        )
    )
)

# Execute the command
print(dispatcher.execute("pow 2", {}))
print(dispatcher.execute("pow 3 4", {}))
```

## Using a custom argument type
```py
from brigadier import CommandDispatcher
from brigadier.builder import literal, argument
from brigadier.suggestion import empty_suggestion

class Vector3:
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z
    
    def parse(self, reader):
        self.x = reader.read_int()
        reader.skip()
        self.y = reader.read_int()
        reader.skip()
        self.z = reader.read_int()
        return self
    
    def list_suggestions(self, builder):
        return empty_suggestion()
    
    def get_examples(self):
        return ["2 3 1", "0 5 0"]

def teleport_command(ctx):
    location = ctx.get_argument("location")
    x = location.x
    y = location.y
    z = location.z
    print(f"You've been teleported to {x}, {y}, {z}")
    return 1

dispatcher = CommandDispatcher()
dispatcher.register(
    literal("teleport").then(
        argument("location", Vector3()).executes()
    )
)

dispatcher.execute("teleport 24 51 -632", {})
```

## License
--------
[MIT](https://github.com/thelennylord/brigadier.py/blob/master/LICENSE)
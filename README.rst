Ecys
====
**Ecys is a simple realization of Entity Components System**

Ecys is an MIT licendes Entity Component System (ECS).
The design is based on *anax* realization of ECS.

1) Compatibility
----------------
Esyc is a Python 3 library only. Specifically, all currently supported versions of Python 3.


2) Installation
---------------
You can install ecys using *pip*::

    pip install ecys


3) Structure
-------------
* World

A World is your main working object to interact with ecys.
After creating a World object, you'll use that object to crate Entities
from your Component objects. A World is assigned all of your System
instances. A World allows you to update all your Systems using call per frame.
You can create or delete Entities, add or remove Systems while your
application is running.


* Entity

Entity is a simple container for Components. You can add or remove
Components from your Entity.


* Components

You should define your Component classes. The should not contain
any logic. Components might have initialization code, but no
updating state logic. You can use *ecys.Component* to indicate your
class as Component, but it's not obligatory.

Example of simple Velocity component::

    @dataclass
    class Velocity(ecys.Component):
        x: float
        y: float


* Systems

Systems are where all processing logic is executed. All Systems must
inherit from the *ecys.System* class, and have a method called *update*.
You should add your System to the World instance to using.
You should define your System classes with *ecys.requires* or
*ecys.excludes* decorators. A *required_entities* method will return
tuple of Entities with (or without) Components specified in decorator
parameters.

A simple RenderSystem::

    @ecys.requires(Position, Velocity)
    class MovementSystem(ecys.System):

        def update(self):
            for entity in self.required_entities:
                position = entity.get_component(Position)
                velocity = entity.get_component(Velocity)
                position.x += velocity.x
                position.y += velocity.y


4) Basic usage
--------------
The first step after importing ecys is to create a World instance::

    world = ecys.World()


Create some System instances and add to the World. You can specify
an optional updating priority (higher number = faster). By default
priority is 0::

    movement_system = MovementSystem()
    render_system = RenderSystem()
    world.add_system(movement_system, 1)
    world.add_system(render_system)
    # . . .
    world.add_system(AnotherOneSystem())


Create Entites::

    player = world.create_entity(Position(0, 0), Velocity(1, 2))
    # . . .
    player.add_component(AnotherOneComponent(*args))


Executing all Systems is done with a single call to *world.update*. This
will call the update methods on all added Systems, in order of their priority::

    world.update()


You can pass any args you need to *world.update*, but you must also make sure to receive
them properly in the *update* methods of your Systems. For example, if you pass a delta time
argument as *world.update(delta_time)*, your Systems's *update* methods should all receive it as:
*def process(self, delta_time):*
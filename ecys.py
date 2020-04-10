from abc import ABC, abstractmethod


__version__ = '2.0.0'


class FilterDecorator(ABC):
    """Abstract base decorator to filter entities in System class."""
    def __init__(self, *component_types):
        self.component_types = component_types

    def __call__(self, system_class):
        system_class.__clauses__ = self._clauses
        return system_class

    @abstractmethod
    def _clauses(self, entity):
        pass


class requires(FilterDecorator):
    """Decorator adds clauses to System class to filter
    entities with required components.
    """

    def _clauses(self, entity):
        return entity.has_components(*self.component_types)


class excludes(FilterDecorator):
    """Decorator adds clauses to System class to filter
    entities without excluded components.
    """

    def _clauses(self, entity):
        return not any(
            ct in entity._components for ct in self.component_types
        )


class Component:
    """Base empty class for all Components to inherit from."""

    def __repr__(self):
        return self.__class__.__name__


class System(ABC):
    """Base class for all Systems to inherit from.

    System instance must contain an `update` method. This method
    will be call by each call to `World.update`.

    System subclass must be declared with filter decorator to add
    __clauses__ because entities property returns entities
    with components according to __clauses__. By default entities
    returns all entities in a World instance.

    Example of overriding `update' method:
    for entity in self.entities:
        a = entity.get_component(ComponentA)
        b = entity.get_component(ComponentB)
        do_some_work(a, b)
        . . .

    """

    __clauses__ = None

    def __init__(self):
        self.world = None
        self.priority = None

    @property
    def entities(self):
        assert self.world, 'No world for this System'
        return self.world.filtered_entities(self.__clauses__)

    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class Entity:
    """Class container for Component objects.

    Do not use `__init__` method. Entities must be created by
    World instance.
    """

    def __init__(self, id, world, *components):
        self._id = id
        assert isinstance(world, World), 'world is not instance of World class'
        self.world = world
        self._components = {type(c): c for c in components}

    def __repr__(self):
        return f'Entity({", ".join(str(c) for c in self.components)})'

    def __eq__(self, other):
        self._id = other.id

    def __hash__(self):
        return hash(self._id)

    @property
    def components(self):
        return tuple(self._components.values())

    def add_component(self, component):
        self._components[type(component)] = component

    def remove_component(self, component_type):
        return self._components.pop(component_type)

    def get_component(self, component_type):
        return self._components[component_type]

    def has_component(self, component_type):
        return component_type in self._components

    def has_components(self, *component_types):
        return all(ct in self._components for ct in component_types)


class World:
    """A World object keeps track of all Entities and Systems.

    Method `update` updates every included system in order
    according to priority.
    """

    def __init__(self):
        self._systems = []
        self._next_entity_id = 0
        self._entities = set()
        self._dead_entities = set()

    def add_system(self, system, priority=0):
        assert issubclass(system.__class__, System),\
            'system class is not subclass of System'
        system.world = self
        system.priority = priority
        self._systems.append(system)
        self._systems.sort(key=lambda sys: sys.priority, reverse=True)

    def remove_system(self, system_type):
        for system in self._systems:
            if type(system) == system_type:
                system.world = None
                system.priority = None
                self._systems.remove(system)

    def get_system(self, system_type):
        for system in self._systems:
            if type(system) == system_type:
                return system

    def create_entity(self, *components):
        self._next_entity_id += 1
        entity = Entity(self._next_entity_id, self, *components)
        self._entities.add(entity)
        return entity

    def delete_entity(self, entity, immediate=False):
        if immediate:
            self._entities.remove(entity)
        else:
            self._dead_entities.add(entity)

    def filtered_entities(self, clauses):
        if clauses is None:
            return tuple(self._entities)
        return tuple(e for e in self._entities if clauses(e))

    def entities_with(self, *components):
        return tuple(
            e for e in self._entities if
            e.has_components(*components)
        )

    def update(self, *args, **kwargs):
        self._delete_dead_entities()
        for system in self._systems:
            system.update(*args, **kwargs)

    def clear(self):
        self._next_entity_id = 0
        self._entities.clear()
        self._dead_entities.clear()

    def _delete_dead_entities(self):
        for entity in self._dead_entities:
            self._entities.remove(entity)
        self._dead_entities.clear()

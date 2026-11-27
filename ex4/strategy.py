from abc import ABC, abstractmethod

from ex3.capability import TransformCapability
from ex3.creature import Creature


class InvalidCreatureError(Exception):
    """Raised when a creature cannot use a battle strategy."""


class BattleStrategy(ABC):
    name: str = "Strategy"

    @abstractmethod
    def act(self, creature: Creature) -> None: ...

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...


class NormalStrategy(BattleStrategy):
    name = "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidCreatureError(
                f"Invalid Creature '{creature.name}' for this normal strategy"
            )
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    name = "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise InvalidCreatureError(
                f"Invalid Creature '{creature.name}' for this "
                "aggressive strategy"
            )
        creature.transform()
        print(creature.attack())
        creature.revert()

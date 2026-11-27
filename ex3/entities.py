from .capability import TransformCapability
from .creature import Creature


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return "Flameling uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return "Pyrodon uses Flamethrower!"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        return self._attack_message(
            "Shiftling attacks normally.",
            "Shiftling performs a boosted strike!",
        )

    def transform(self) -> None:
        self._transformed = True
        print("Shiftling shifts into a sharper form!")

    def revert(self) -> None:
        self._transformed = False
        print("Shiftling returns to normal.")


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        return self._attack_message(
            "Morphagon attacks normally.",
            "Morphagon unleashes a devastating morph strike!",
        )

    def transform(self) -> None:
        self._transformed = True
        print("Morphagon morphs into a dragonic battle form!")

    def revert(self) -> None:
        self._transformed = False
        print("Morphagon stabilizes its form.")

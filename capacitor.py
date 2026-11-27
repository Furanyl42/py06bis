from ex3 import TransformCreatureFactory
from ex3.capability import TransformCapability
from ex3.creature import Creature


def show_transform(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if not isinstance(creature, TransformCapability):
        return
    creature.transform()
    print(creature.attack())
    creature.revert()


def main() -> None:
    factory = TransformCreatureFactory()

    print("Testing Creature with transform capability")
    print(" base:")
    show_transform(factory.create_base())
    print(" evolved:")
    show_transform(factory.create_evolved())


if __name__ == "__main__":
    main()

from picasso.models import Floor, Color, Animal
from picasso.picasso_tower import PicassoTower


class Hint(object):
    """Base class for all the hint classes"""

    pass


class SpecificHint(Hint):
    def validate(self, picasso_tower: PicassoTower) -> bool:
        pass


class AbsoluteHint(Hint):
    """
    Represents a hint on a specific floor. Examples:
    The third floor is red:
        AbsoluteHint(Floor.Third, Color.Red)
    The frog lives on the fifth floor:
        AbsoluteHint(Animal.Frog, Floor.Fifth)
    The orange floor is the floor where the chicken lives:
        AbsoluteHint(Color.Orange, Animal.Chicken)
    """

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


class FloorColorAbsoluteHint(SpecificHint):
    def __init__(self, floor: Floor, color: Color):
        self.floor = floor
        self.color = color

    def validate(self, picasso_tower: PicassoTower) -> bool:
        return picasso_tower.floors[self.floor].color == self.color


class FloorAnimalAbsoluteHint(SpecificHint):
    def __init__(self, floor: Floor, animal: Animal):
        self.floor = floor
        self.animal = animal

    def validate(self, picasso_tower: PicassoTower) -> bool:
        return picasso_tower.floors[self.floor].animal == self.animal


class ColorAnimalAbsoluteHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal):
        self.color = color
        self.animal = animal

    def validate(self, picasso_tower: PicassoTower) -> bool:
        for floor in picasso_tower.floors.values():
            if floor.color == self.color and floor.animal == self.animal:
                return True
        return False


class RelativeHint(Hint):
    """
    Represents a hint of a relation between two floor
    that are of a certain distance of each other.
    Examples:
    The red floor is above the blue floor:
        RelativeHint(Color.Red, Color.Red, 1)
    The frog lives three floor below the yellow floor:
        RelativeHint(Animal.Frog, Color.Yellow, -3)
    The third floor is two floors below the fifth floor:
        RelativeHint(Floor.Third, Floor.Fifth, -2)
    """

    def __init__(self, attr1, attr2, difference):
        self.attr1 = attr1
        self.attr2 = attr2
        self.difference = difference


class FloorFloorRelativeHint(SpecificHint):
    def __init__(self, floor1: Floor, floor2: Floor, difference: int):
        self.floor1 = floor1
        self.floor2 = floor2
        self.difference = difference

    def validate(self, picasso_tower: PicassoTower) -> bool:
        return picasso_tower.floors[self.floor2 + self.difference] == picasso_tower.floors[self.floor1]


class ColorColorRelativeHint(SpecificHint):
    def __init__(self, color1: Color, color2: Color, difference: int):
        self.color1 = color1
        self.color2 = color2
        self.difference = difference

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.difference < 0:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].color == self.color1
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].color == self.color2
                ):
                    return True
        else:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].color == self.color2
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].color == self.color1
                ):
                    return True
        return False


class ColorAnimalRelativeHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal, difference: int):
        self.color = color
        self.animal = animal
        self.difference = difference

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.difference < 0:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].color == self.color
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].animal == self.animal
                ):
                    return True
        else:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].animal == self.animal
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].color == self.color
                ):
                    return True
        return False


class AnimalAnimalRelativeHint(SpecificHint):
    def __init__(self, animal1: Animal, animal2: Animal, difference: int):
        self.animal1 = animal1
        self.animal2 = animal2
        self.difference = difference

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.difference < 0:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].animal == self.animal1
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].animal == self.animal2
                ):
                    return True
        else:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].animal == self.animal2
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].color == self.animal1
                ):
                    return True
        return False


class AnimalColorRelativeHint(SpecificHint):
    def __init__(self, animal: Animal, color: Color, difference: int):
        self.animal = animal
        self.color = color
        self.difference = difference

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.difference < 0:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].animal == self.animal
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].color == self.color
                ):
                    return True
        else:
            for floor_number in range(1, len(picasso_tower.floors) - abs(self.difference) + 1):
                if (
                    picasso_tower.floors[Floor(floor_number)].color == self.color
                    and picasso_tower.floors[Floor(floor_number + abs(self.difference))].animal == self.animal
                ):
                    return True
        return False


class NeighborHint(Hint):
    """
    Represents a hint of a relation between two floors that are adjacent
    (first either above or below the second).
    Examples:
    The green floor is neighboring the floor where the chicken lives:
        NeighborHint(Color.Green, Animal.Chicken)
    The grasshopper is a neighbor of the rabbit:
        NeighborHint(Animal.Grasshopper, Animal.Rabbit)
    The yellow floor is neighboring the third floor:
        NeighborHint(Color.Yellow, Floor.Third)
    """

    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


class FloorColorNeighborHint(SpecificHint):
    def __init__(self, floor: Floor, color: Color):
        self.floor = floor
        self.color = color

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.floor == Floor.First:
            return picasso_tower.floors[self.floor + 1].color == self.color
        if self.floor == Floor.Fifth:
            return picasso_tower.floors[self.floor + -1].color == self.color
        return (picasso_tower.floors[self.floor + 1].color == self.color) or (
            picasso_tower.floors[self.floor - 1].color == self.color
        )


class FloorAnimalNeighborHint(SpecificHint):
    def __init__(self, floor: Floor, animal: Animal):
        self.floor = floor
        self.animal = animal

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if self.floor == Floor.First:
            return picasso_tower.floors[self.floor + 1].animal == self.animal
        if self.floor == Floor.Fifth:
            return picasso_tower.floors[self.floor + -1].animal == self.animal
        return (picasso_tower.floors[self.floor + 1].animal == self.animal) or (
            picasso_tower.floors[self.floor - 1].animal == self.animal
        )


class ColorColorNeighborHint(SpecificHint):
    def __init__(self, color1: Color, color2: Color):
        self.color1 = color1
        self.color2 = color2

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if (
            picasso_tower.floors[Floor.First].color == self.color1
            and picasso_tower.floors[Floor.First + 1].color == self.color2
        ):
            return True
        if (
            picasso_tower.floors[Floor.Fifth].color == self.color1
            and picasso_tower.floors[Floor.Fifth - 1].color == self.color2
        ):
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if picasso_tower.floors[Floor(floor_number)].color == self.color1 and (
                picasso_tower.floors[Floor(floor_number) - 1].color == self.color2
                or picasso_tower.floors[Floor(floor_number) + 1].color == self.color2
            ):
                return True
        return False


class ColorAnimalNeighborHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal):
        self.color = color
        self.animal = animal

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if (
            picasso_tower.floors[Floor.First].color == self.color
            and picasso_tower.floors[Floor.First + 1].animal == self.animal
        ):
            return True
        if (
            picasso_tower.floors[Floor.Fifth].color == self.color
            and picasso_tower.floors[Floor.Fifth - 1].animal == self.animal
        ):
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if picasso_tower.floors[Floor(floor_number)].color == self.color and (
                picasso_tower.floors[Floor(floor_number) - 1].animal == self.animal
                or picasso_tower.floors[Floor(floor_number) + 1].animal == self.animal
            ):
                return True
        return False


class AnimalAnimalNeighborHint(SpecificHint):
    def __init__(self, animal1: Animal, animal2: Animal):
        self.animal1 = animal1
        self.animal2 = animal2

    def validate(self, picasso_tower: PicassoTower) -> bool:
        if (
            picasso_tower.floors[Floor.First].animal == self.animal1
            and picasso_tower.floors[Floor.First + 1].animal == self.animal2
        ):
            return True
        if (
            picasso_tower.floors[Floor.Fifth].animal == self.animal1
            and picasso_tower.floors[Floor.Fifth - 1].animal == self.animal2
        ):
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if picasso_tower.floors[Floor(floor_number)].animal == self.animal1 and (
                picasso_tower.floors[Floor(floor_number) - 1].animal == self.animal2
                or picasso_tower.floors[Floor(floor_number) + 1].animal == self.animal2
            ):
                return True
        return False


def get_specific_absolute_hint(hint: AbsoluteHint) -> SpecificHint:
    if isinstance(hint.attr1, Floor):
        if isinstance(hint.attr2, Color):
            return FloorColorAbsoluteHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Animal):
            return FloorAnimalAbsoluteHint(hint.attr1, hint.attr2)

    elif isinstance(hint.attr1, Color):
        if isinstance(hint.attr2, Animal):
            return ColorAnimalAbsoluteHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Floor):
            return FloorColorAbsoluteHint(hint.attr2, hint.attr1)

    elif isinstance(hint.attr1, Animal):
        if isinstance(hint.attr2, Floor):
            return FloorAnimalAbsoluteHint(hint.attr2, hint.attr1)
        if isinstance(hint.attr2, Color):
            return ColorAnimalAbsoluteHint(hint.attr2, hint.attr1)

    raise ValueError(f"Got bad hint attr class, can only be one of {Floor, Color, Animal}")


def get_specific_relative_hint(hint: RelativeHint) -> SpecificHint:
    if isinstance(hint.attr1, Floor):
        if isinstance(hint.attr2, Floor):
            return FloorFloorRelativeHint(hint.attr1, hint.attr2, hint.difference)

    elif isinstance(hint.attr1, Color):
        if isinstance(hint.attr2, Color):
            return ColorColorRelativeHint(hint.attr1, hint.attr2, hint.difference)
        if isinstance(hint.attr2, Animal):
            return ColorAnimalRelativeHint(hint.attr1, hint.attr2, hint.difference)

    elif isinstance(hint.attr1, Animal):
        if isinstance(hint.attr2, Animal):
            return AnimalAnimalRelativeHint(hint.attr1, hint.attr2, hint.difference)
        if isinstance(hint.attr2, Color):
            return AnimalColorRelativeHint(hint.attr1, hint.attr2, hint.difference)

    raise ValueError(f"Got bad hint attr class, can only be one of {Floor, Color, Animal}")


def get_specific_neighbor_hint(hint: NeighborHint) -> SpecificHint:
    if isinstance(hint.attr1, Floor):
        if isinstance(hint.attr2, Color):
            return FloorColorNeighborHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Animal):
            return FloorAnimalNeighborHint(hint.attr1, hint.attr2)

    elif isinstance(hint.attr1, Color):
        if isinstance(hint.attr2, Color):
            return ColorColorNeighborHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Animal):
            return ColorAnimalNeighborHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Floor):
            return FloorColorNeighborHint(hint.attr2, hint.attr1)

    elif isinstance(hint.attr1, Animal):
        if isinstance(hint.attr2, Animal):
            return AnimalAnimalNeighborHint(hint.attr1, hint.attr2)
        if isinstance(hint.attr2, Floor):
            return FloorAnimalNeighborHint(hint.attr2, hint.attr1)
        if isinstance(hint.attr2, Color):
            return ColorAnimalNeighborHint(hint.attr2, hint.attr1)

    raise ValueError(f"Got bad hint attr class, can only be one of {Floor, Color, Animal}")


def get_specific_hints(hints: list[Hint]) -> list[SpecificHint]:
    specific_hints: list[SpecificHint] = []
    for hint in hints:
        if isinstance(hint, AbsoluteHint):
            specific_hints.append(get_specific_absolute_hint(hint))
        elif isinstance(hint, RelativeHint):
            specific_hints.append(get_specific_relative_hint(hint))
        elif isinstance(hint, NeighborHint):
            specific_hints.append(get_specific_neighbor_hint(hint))
        else:
            raise ValueError(f"Got bad hint class, can only be one of {AbsoluteHint, RelativeHint, NeighborHint}")
    return specific_hints
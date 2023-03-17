from picasso.hints_utils import complete_last_available_absolute_color_animal_hint
from picasso.models import Animal, Color, Floor, PicassoTowerFloor


class Hint(object):
    """Base class for all the hint classes"""

    pass


class SpecificHint(Hint):
    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        raise NotImplementedError

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        raise NotImplementedError


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

    def __init__(self, attr1: Floor | Color | Animal, attr2: Floor | Color | Animal):
        self.attr1 = attr1
        self.attr2 = attr2


class FloorColorAbsoluteHint(SpecificHint):
    def __init__(self, floor: Floor, color: Color):
        self.floor = floor
        self.color = color

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        return floors[self.floor].color == self.color

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        floors[self.floor].color = self.color


class FloorAnimalAbsoluteHint(SpecificHint):
    def __init__(self, floor: Floor, animal: Animal):
        self.floor = floor
        self.animal = animal

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        return floors[self.floor].animal == self.animal

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        floors[self.floor].animal = self.animal


class ColorAnimalAbsoluteHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal):
        self.color = color
        self.animal = animal

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        for floor in floors.values():
            if floor.color == self.color and floor.animal == self.animal:
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        for floor in floors.values():
            if floor.color == self.color:
                floor.animal = self.animal
            elif floor.animal == self.animal:
                floor.color = self.color
        complete_last_available_absolute_color_animal_hint(floors, self.color, self.animal)


class RelativeHint(Hint):
    """
    Represents a hint of a relation between two floor
    that are of a certain distance of each other.
    Examples:
    The red floor is above the blue floor:
        RelativeHint(Color.Red, Color.Blue, 1)
    The frog lives three floor below the yellow floor:
        RelativeHint(Animal.Frog, Color.Yellow, -3)
    The third floor is two floors below the fifth floor:
        RelativeHint(Floor.Third, Floor.Fifth, -2)
    """

    def __init__(self, attr1: Floor | Color | Animal, attr2: Floor | Color | Animal, difference: int):
        self.attr1 = attr1
        self.attr2 = attr2
        self.difference = difference


class ColorColorRelativeHint(SpecificHint):
    def __init__(self, color1: Color, color2: Color, difference: int):
        self.color1 = color1
        self.color2 = color2
        self.difference = difference

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if (
                floors[Floor(floor_number)].color == self.color1
                and floors[Floor(floor_number - self.difference)].color == self.color2
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if floors[Floor(floor_number)].color == self.color1:
                floors[Floor(floor_number - self.difference)].color = self.color2
            elif floors[Floor(floor_number - self.difference)].color == self.color2:
                floors[Floor(floor_number)].color = self.color1


class ColorAnimalRelativeHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal, difference: int):
        self.color = color
        self.animal = animal
        self.difference = difference

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if (
                floors[Floor(floor_number)].color == self.color
                and floors[Floor(floor_number - self.difference)].animal == self.animal
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if floors[Floor(floor_number)].color == self.color:
                floors[Floor(floor_number - self.difference)].animal = self.animal
            elif floors[Floor(floor_number - self.difference)].animal == self.animal:
                floors[Floor(floor_number)].color = self.color


class AnimalAnimalRelativeHint(SpecificHint):
    def __init__(self, animal1: Animal, animal2: Animal, difference: int):
        self.animal1 = animal1
        self.animal2 = animal2
        self.difference = difference

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if (
                floors[Floor(floor_number)].animal == self.animal1
                and floors[Floor(floor_number - self.difference)].animal == self.animal2
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if floors[Floor(floor_number)].animal == self.animal1:
                floors[Floor(floor_number - self.difference)].animal = self.animal2
            elif floors[Floor(floor_number - self.difference)].animal == self.animal2:
                floors[Floor(floor_number)].animal = self.animal1


class AnimalColorRelativeHint(SpecificHint):
    def __init__(self, animal: Animal, color: Color, difference: int):
        self.animal = animal
        self.color = color
        self.difference = difference

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if (
                floors[Floor(floor_number)].animal == self.animal
                and floors[Floor(floor_number - self.difference)].color == self.color
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        for floor_number in range(max(0, self.difference) + 1, min(len(floors) + self.difference, len(floors)) + 1):
            if floors[Floor(floor_number)].animal == self.animal:
                floors[Floor(floor_number - self.difference)].color = self.color
            elif floors[Floor(floor_number - self.difference)].color == self.color:
                floors[Floor(floor_number)].animal = self.animal


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

    def __init__(self, attr1: Floor | Color | Animal, attr2: Floor | Color | Animal):
        self.attr1 = attr1
        self.attr2 = attr2


class FloorColorNeighborHint(SpecificHint):
    def __init__(self, floor: Floor, color: Color):
        self.floor = floor
        self.color = color

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        if self.floor == Floor.First:
            return floors[Floor.Second].color == self.color
        if self.floor == Floor.Fifth:
            return floors[Floor.Fourth].color == self.color
        return (floors[Floor(self.floor + 1)].color == self.color) or (
            floors[Floor(self.floor - 1)].color == self.color
        )

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        if self.floor == Floor.First:
            floors[Floor.Second].color = self.color
        elif self.floor == Floor.Fifth:
            floors[Floor.Fourth].color = self.color
        elif floors[Floor(self.floor + 1)].color is None:
            floors[Floor(self.floor - 1)].color = self.color
        elif floors[Floor(self.floor - 1)].color is None:
            floors[Floor(self.floor + 1)].color = self.color


class FloorAnimalNeighborHint(SpecificHint):
    def __init__(self, floor: Floor, animal: Animal):
        self.floor = floor
        self.animal = animal

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        if self.floor == Floor.First:
            return floors[Floor.Second].animal == self.animal
        if self.floor == Floor.Fifth:
            return floors[Floor.Fourth].animal == self.animal
        return (floors[Floor(self.floor + 1)].animal == self.animal) or (
            floors[Floor(self.floor - 1)].animal == self.animal
        )

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        if self.floor == Floor.First:
            floors[Floor.Second].animal = self.animal
        elif self.floor == Floor.Fifth:
            floors[Floor.Fourth].animal = self.animal
        elif floors[Floor(self.floor + 1)].animal is None:
            floors[Floor(self.floor - 1)].animal = self.animal
        elif floors[Floor(self.floor - 1)].animal is None:
            floors[Floor(self.floor + 1)].animal = self.animal


class ColorColorNeighborHint(SpecificHint):
    def __init__(self, color1: Color, color2: Color):
        self.color1 = color1
        self.color2 = color2

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        if floors[Floor.First].color == self.color1 and floors[Floor(Floor.First + 1)].color == self.color2:
            return True
        if floors[Floor.Fifth].color == self.color1 and floors[Floor(Floor.Fifth - 1)].color == self.color2:
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if floors[Floor(floor_number)].color == self.color1 and (
                floors[Floor(floor_number - 1)].color == self.color2
                or floors[Floor(floor_number + 1)].color == self.color2
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        if floors[Floor.First].color in [self.color1, self.color2]:
            floors[Floor.Second].color = self.color1 if floors[Floor.First].color == self.color2 else self.color2
        elif floors[Floor.Fifth].color in [self.color1, self.color2]:
            floors[Floor.Fourth].color = self.color1 if floors[Floor.Fifth].color == self.color2 else self.color2
        else:
            for floor_number in range(Floor.Second, Floor.Fifth):
                if floors[Floor(floor_number)].color in [self.color1, self.color2]:
                    color_to_insert = self.color1 if floors[Floor(floor_number)].color == self.color2 else self.color2
                    if floors[Floor(floor_number + 1)].color is None:
                        floors[Floor(floor_number - 1)].color = color_to_insert
                    elif floors[Floor(floor_number - 1)].color is None:
                        floors[Floor(floor_number + 1)].color = color_to_insert


class ColorAnimalNeighborHint(SpecificHint):
    def __init__(self, color: Color, animal: Animal):
        self.color = color
        self.animal = animal

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        if floors[Floor.First].color == self.color and floors[Floor(Floor.First + 1)].animal == self.animal:
            return True
        if floors[Floor.Fifth].color == self.color and floors[Floor(Floor.Fifth - 1)].animal == self.animal:
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if floors[Floor(floor_number)].color == self.color and (
                floors[Floor(floor_number - 1)].animal == self.animal
                or floors[Floor(floor_number + 1)].animal == self.animal
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        if floors[Floor.First].color == self.color:
            floors[Floor.Second].animal = self.animal
        elif floors[Floor.First].animal == self.animal:
            floors[Floor.Second].color = self.color

        elif floors[Floor.Fifth].color == self.color:
            floors[Floor.Fourth].animal = self.animal
        elif floors[Floor.Fifth].animal == self.animal:
            floors[Floor.Fourth].color = self.color

        else:
            for floor_number in range(Floor.Second, Floor.Fifth):
                if floors[Floor(floor_number)].color == self.color:
                    if floors[Floor(floor_number + 1)].animal is None:
                        floors[Floor(floor_number - 1)].animal = self.animal
                    elif floors[Floor(floor_number - 1)].animal is None:
                        floors[Floor(floor_number + 1)].animal = self.animal
                elif floors[Floor(floor_number)].animal == self.animal:
                    if floors[Floor(floor_number + 1)].color is None:
                        floors[Floor(floor_number - 1)].color = self.color
                    elif floors[Floor(floor_number - 1)].color is None:
                        floors[Floor(floor_number + 1)].color = self.color


class AnimalAnimalNeighborHint(SpecificHint):
    def __init__(self, animal1: Animal, animal2: Animal):
        self.animal1 = animal1
        self.animal2 = animal2

    def validate(self, floors: dict[Floor, PicassoTowerFloor]) -> bool:
        if floors[Floor.First].animal == self.animal1 and floors[Floor(Floor.First + 1)].animal == self.animal2:
            return True
        if floors[Floor.Fifth].animal == self.animal1 and floors[Floor(Floor.Fifth - 1)].animal == self.animal2:
            return True
        for floor_number in range(Floor.Second, Floor.Fifth):
            if floors[Floor(floor_number)].animal == self.animal1 and (
                floors[Floor(floor_number - 1)].animal == self.animal2
                or floors[Floor(floor_number + 1)].animal == self.animal2
            ):
                return True
        return False

    def insert(self, floors: dict[Floor, PicassoTowerFloor]) -> None:
        if floors[Floor.First].animal in [self.animal1, self.animal2]:
            floors[Floor.Second].animal = self.animal1 if floors[Floor.First].animal == self.animal2 else self.animal2
        elif floors[Floor.Fifth].animal in [self.animal1, self.animal2]:
            floors[Floor.Fourth].animal = self.animal1 if floors[Floor.Fifth].animal == self.animal2 else self.animal2
        else:
            for floor_number in range(Floor.Second, Floor.Fifth):
                if floors[Floor(floor_number)].animal in [self.animal1, self.animal2]:
                    animal_to_insert = (
                        self.animal1 if floors[Floor(floor_number)].animal == self.animal2 else self.animal2
                    )
                    if floors[Floor(floor_number + 1)].animal is None:
                        floors[Floor(floor_number - 1)].animal = animal_to_insert
                    elif floors[Floor(floor_number - 1)].animal is None:
                        floors[Floor(floor_number + 1)].animal = animal_to_insert


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
    if isinstance(hint.attr1, Color):
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

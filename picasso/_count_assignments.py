from itertools import permutations, product
from typing import Generator

from picasso.hints import AbsoluteHint, Hint, NeighborHint, RelativeHint, SpecificHint, get_specific_hints
from picasso.hints_utils import complete_last_available_option
from picasso.models import Animal, Color, Floor, PicassoTowerFloor


def generate_all_floor_combinations(floors_number: int) -> Generator[dict[Floor, PicassoTowerFloor], None, None]:
    """
    TODO: Improve this
    """
    floors: dict[Floor, PicassoTowerFloor] = {
        Floor(i + 1): PicassoTowerFloor(animal=None, color=None) for i in range(floors_number)
    }
    for animal_perm in permutations(Animal, floors_number):
        for color_perm in permutations(Color, floors_number):
            for i, floor in enumerate(floors.values()):
                floor.animal = animal_perm[i]
                floor.color = color_perm[i]
            yield floors


def generate_all_floor_combinations2(
    floors: dict[Floor, PicassoTowerFloor],
    unused_colors: set[Color] | None = None,
    unused_animals: set[Animal] | None = None,
) -> Generator[dict[Floor, PicassoTowerFloor], None, None]:
    if unused_colors is None:
        unused_colors = set(Color) - {floor.color for floor in floors.values() if floor.color is not None}
    if unused_animals is None:
        unused_animals = set(Animal) - {floor.animal for floor in floors.values() if floor.animal is not None}

    if not unused_animals and not unused_colors:
        yield floors
        return

    new_floors = floors.copy()
    for floor_number, floor in new_floors.items():
        if floor.color is None or floor.animal is None:
            floor_possible_color = {floor.color} if floor.color is not None else unused_colors
            floor_possible_animal = {floor.animal} if floor.animal is not None else unused_animals
            for color, animal in product(floor_possible_color, floor_possible_animal):
                new_floors[floor_number] = PicassoTowerFloor(color=color, animal=animal)

                new_unused_colors = unused_colors.copy()
                new_unused_colors.remove(color)
                new_unused_animals = unused_animals.copy()
                new_unused_animals.remove(animal)

                yield from generate_all_floor_combinations2(
                    floors=new_floors, unused_colors=new_unused_colors, unused_animals=new_unused_animals
                )


def generate_all_floor_combinations3(
    floors: dict[Floor, PicassoTowerFloor]
) -> Generator[dict[Floor, PicassoTowerFloor], None, None]:
    unused_colors = list(Color)
    unused_animals = list(Animal)

    for floor in floors.values():
        if floor.color in unused_colors:
            unused_colors.remove(floor.color)
        if floor.animal in unused_animals:
            unused_animals.remove(floor.animal)

    for color_perm in permutations(unused_colors):
        for animal_perm in permutations(unused_animals):
            color_iter = iter(color_perm)
            animal_iter = iter(animal_perm)
            floors_copy = {
                floor_num: PicassoTowerFloor(animal=floors[floor_num].animal, color=floors[floor_num].color)
                for floor_num in floors
            }
            for floor in floors_copy.values():
                if floor.color is None:
                    floor.color = next(color_iter)
                if floor.animal is None:
                    floor.animal = next(animal_iter)
            yield floors_copy


def insert_hints(floors: dict[Floor, PicassoTowerFloor], hints: list[SpecificHint]) -> None:
    for hint in hints:
        hint.insert(floors)

    complete_last_available_option(floors)
    # TODO Add completion of last available relative hint


def count_assignments(hints: list[Hint]) -> int:
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
    """
    counter = 0
    specific_hints = get_specific_hints(hints)
    floors: dict[Floor, PicassoTowerFloor] = {
        Floor(i + 1): PicassoTowerFloor(animal=None, color=None) for i in range(5)
    }
    insert_hints(floors, specific_hints)
    for floors_combination in generate_all_floor_combinations3(floors=floors):
        for specific_hint in specific_hints:
            if not specific_hint.validate(floors_combination):
                break
        else:
            counter += 1
    return counter


HINTS_EX1 = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    NeighborHint(Color.Yellow, Color.Green),
]

HINTS_EX2 = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Floor.First, Color.Green),
    AbsoluteHint(Animal.Frog, Color.Yellow),
    NeighborHint(Animal.Frog, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Orange),
    RelativeHint(Animal.Chicken, Color.Blue, -4),
]

HINTS_EX3: list[Hint] = [RelativeHint(Animal.Rabbit, Color.Green, -2)]

HINTS_EX4: list[Hint] = []


def test() -> None:
    assert count_assignments(HINTS_EX1) == 2, "Failed on example #1"
    assert count_assignments(HINTS_EX2) == 4, "Failed on example #2"
    assert count_assignments(HINTS_EX3) == 1728, "Failed on example #3"
    assert count_assignments(HINTS_EX4) == 14400, "Failed on example #4"
    print("Success!")


if __name__ == "__main__":
    test()

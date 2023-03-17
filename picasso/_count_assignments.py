from itertools import permutations
from typing import Generator

from picasso.hints import Hint, SpecificHint, get_specific_hints
from picasso.hints_utils import complete_last_available_option
from picasso.models import Animal, Color, Floor, PicassoTowerFloor


def generate_all_floor_combinations(
    tower: dict[Floor, PicassoTowerFloor]
) -> Generator[dict[Floor, PicassoTowerFloor], None, None]:
    """
    Generate all possible assignments of the tower.
    Take in consideration the already existing information in the tower.
    The logic is to go over all unused colors permutations and for each one go over all unused animals permutations,
    then go over the tower floors and for each empty space insert the next color/animal
    according to the current permutations.
    """
    unused_colors = list(Color)
    unused_animals = list(Animal)

    for floor in tower.values():
        if floor.color in unused_colors:
            unused_colors.remove(floor.color)
        if floor.animal in unused_animals:
            unused_animals.remove(floor.animal)

    for color_perm in permutations(unused_colors):
        for animal_perm in permutations(unused_animals):
            color_iter = iter(color_perm)
            animal_iter = iter(animal_perm)
            floors_copy = {
                floor_num: PicassoTowerFloor(animal=tower[floor_num].animal, color=tower[floor_num].color)
                for floor_num in tower
            }
            for floor in floors_copy.values():
                if floor.color is None:
                    floor.color = next(color_iter)
                if floor.animal is None:
                    floor.animal = next(animal_iter)
            yield floors_copy


def insert_hints(tower: dict[Floor, PicassoTowerFloor], hints: list[SpecificHint]) -> None:
    """
    Responsible for inserting color and animal to the floors according to the hints.
    """
    for hint in hints:
        hint.insert(tower)

    complete_last_available_option(tower)
    # TODO Add completion of last available relative hint


def count_assignments(hints: list[Hint]) -> int:
    """
    Given a list of Hint objects, return the number of valid assignments that satisfy these hints.
    """
    counter = 0
    specific_hints = get_specific_hints(hints)
    tower: dict[Floor, PicassoTowerFloor] = {Floor(i + 1): PicassoTowerFloor(animal=None, color=None) for i in range(5)}
    insert_hints(tower, specific_hints)
    for floors_combination in generate_all_floor_combinations(tower=tower):
        for specific_hint in specific_hints:
            if not specific_hint.validate(floors_combination):
                break
        else:
            counter += 1
    return counter

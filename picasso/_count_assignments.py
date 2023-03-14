from itertools import permutations
from picasso.models import Floor, Color, Animal
from picasso.hints import Hint, AbsoluteHint, RelativeHint, NeighborHint, get_specific_hints
from picasso.picasso_tower import PicassoTower


def generate_all_floor_combinations(floors_number: int):
    """
    TODO: Improve this
    """
    tower = PicassoTower(floors_number)
    for animal_perm in permutations(Animal, floors_number):
        for color_perm in permutations(Color, floors_number):
            for i, floor in enumerate(tower.floors.values()):
                floor.animal = animal_perm[i]
                floor.color = color_perm[i]
            yield tower


def count_assignments(hints: list[Hint]):
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
    """
    counter = 0
    specific_hints = get_specific_hints(hints)
    for tower in generate_all_floor_combinations(5):
        for specific_hint in specific_hints:
            if not specific_hint.validate(tower):
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
    RelativeHint(Animal.Chicken, Color.Blue, -4)
]

HINTS_EX3 = [
    RelativeHint(Animal.Rabbit, Color.Green, -2)
]


def test():
    assert count_assignments(HINTS_EX1) == 2, 'Failed on example #1'
    assert count_assignments(HINTS_EX2) == 4, 'Failed on example #2'
    assert count_assignments(HINTS_EX3) == 1728, 'Failed on example #3'
    print('Success!')


if __name__ == '__main__':
    test()

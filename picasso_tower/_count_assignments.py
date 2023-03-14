from picasso_tower.models import Floor, Color, Animal
from picasso_tower.hints import Hint, AbsoluteHint, RelativeHint, NeighborHint, get_specific_hints


def count_assignments(hints: list[Hint]):
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
    """
    specific_hints = get_specific_hints(hints)
    return 0


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

import pytest

from picasso._count_assignments import count_assignments
from picasso.hints import AbsoluteHint, Hint, NeighborHint, RelativeHint
from picasso.models import Animal, Color, Floor

TEST_ALMOST_FULL_TOWER = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    NeighborHint(Color.Yellow, Color.Green),
]

TEST_ALL_HINT_TYPES = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Floor.First, Color.Green),
    AbsoluteHint(Animal.Frog, Color.Yellow),
    NeighborHint(Animal.Frog, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Orange),
    RelativeHint(Animal.Chicken, Color.Blue, -4),
]

TEST_SMALL_AMOUNT_OF_HINTS: list[Hint] = [RelativeHint(Animal.Rabbit, Color.Green, -2)]

TEST_NO_HINTS_RESULT_IN_ALL_ASSIGNMENTS_POSSIBLE: list[Hint] = []

TEST_OVERLAPPING_HINTS_RESULT_IN_ZERO_POSSIBLE_ASSIGNMENTS: list[Hint] = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Rabbit, Floor.Fifth),
]

TEST_FULL_TOWER_RESULT_IN_ONE_POSSIBLE_ASSIGNMENT = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    AbsoluteHint(Animal.Chicken, Color.Green),
    NeighborHint(Color.Yellow, Color.Green),
]


TEST_FULL_ANIMAL_HINTS = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Animal.Grasshopper),
    AbsoluteHint(Floor.Fourth, Animal.Bird),
    AbsoluteHint(Animal.Frog, Floor.Fifth),
]

TEST_FULL_COLOR_HINTS = [
    AbsoluteHint(Color.Red, Floor.First),
    AbsoluteHint(Color.Yellow, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Green),
    AbsoluteHint(Floor.Fourth, Color.Orange),
    AbsoluteHint(Color.Blue, Floor.Fifth),
]

TEST_ALL_ABSOLUTE_HINT_KINDS = [
    AbsoluteHint(Color.Red, Floor.First),
    AbsoluteHint(Animal.Bird, Floor.Second),
    AbsoluteHint(Color.Red, Animal.Grasshopper),
    AbsoluteHint(Animal.Bird, Color.Orange),
]

TEST_ALL_RELATIVE_HINT_KINDS = [
    AbsoluteHint(Color.Orange, Floor.First),
    RelativeHint(Color.Orange, Color.Blue, -1),
    RelativeHint(Color.Blue, Animal.Grasshopper, -1),
    RelativeHint(Animal.Grasshopper, Animal.Chicken, 1),
    RelativeHint(Animal.Chicken, Color.Red, -3),
]

TEST_ALL_NEIGHBOR_HINT_KINDS = [
    AbsoluteHint(Color.Red, Floor.First),
    AbsoluteHint(Color.Yellow, Floor.Fifth),
    AbsoluteHint(Animal.Rabbit, Floor.Fifth),
    NeighborHint(Floor.First, Color.Green),
    NeighborHint(Floor.Fifth, Animal.Grasshopper),
    NeighborHint(Floor.Third, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Green),
    NeighborHint(Color.Yellow, Animal.Grasshopper),
    NeighborHint(Animal.Bird, Animal.Grasshopper),
    NeighborHint(Animal.Rabbit, Color.Blue),
]


@pytest.mark.parametrize(
    "hints,expected_count",
    [
        (TEST_ALMOST_FULL_TOWER, 2),
        (TEST_ALL_HINT_TYPES, 4),
        (TEST_SMALL_AMOUNT_OF_HINTS, 1728),
        (TEST_NO_HINTS_RESULT_IN_ALL_ASSIGNMENTS_POSSIBLE, 14400),
        (TEST_OVERLAPPING_HINTS_RESULT_IN_ZERO_POSSIBLE_ASSIGNMENTS, 0),
        (TEST_FULL_TOWER_RESULT_IN_ONE_POSSIBLE_ASSIGNMENT, 1),
        (TEST_FULL_ANIMAL_HINTS, 120),
        (TEST_FULL_COLOR_HINTS, 120),
        (TEST_ALL_ABSOLUTE_HINT_KINDS, 36),
        (TEST_ALL_RELATIVE_HINT_KINDS, 12),
        (TEST_ALL_NEIGHBOR_HINT_KINDS, 2),
    ],
)
def test_count_assignments(hints: list[Hint], expected_count: int) -> None:
    result_count = count_assignments(hints)
    assert result_count == expected_count, f"Test failed, expected count {expected_count} but got {result_count}"

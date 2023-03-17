import pytest

from picasso._count_assignments import count_assignments
from picasso.hints import AbsoluteHint, Hint, NeighborHint, RelativeHint
from picasso.models import Animal, Color, Floor

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

assert count_assignments(HINTS_EX1) == 2, "Failed on example #1"
assert count_assignments(HINTS_EX2) == 4, "Failed on example #2"
assert count_assignments(HINTS_EX3) == 1728, "Failed on example #3"
assert count_assignments(HINTS_EX4) == 14400, "Failed on example #4"


@pytest.mark.parametrize(
    "hints,expected_count", [(HINTS_EX1, 2), (HINTS_EX2, 4), (HINTS_EX3, 1728), (HINTS_EX4, 14400)]
)
def test_count_assignments(hints: list[Hint], expected_count: int) -> None:
    result_count = count_assignments(hints)
    assert result_count == expected_count, f"Test failed, expected count {expected_count} but got {result_count}"

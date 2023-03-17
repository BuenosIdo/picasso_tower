from picasso.models import Animal, Color, Floor, PicassoTowerFloor


def complete_last_available_option(tower: dict[Floor, PicassoTowerFloor]) -> None:
    """
    In cases where there is only one color or animal left to insert,
    this function responsible for inserting those color or animal to the left empty floor space.
    """
    unused_colors = list(Color)
    unused_animals = list(Animal)
    empty_color_floors: list[PicassoTowerFloor] = []
    empty_animal_floors: list[PicassoTowerFloor] = []

    for floor in tower.values():
        if floor.color in unused_colors:
            unused_colors.remove(floor.color)
        if floor.animal in unused_animals:
            unused_animals.remove(floor.animal)
        if floor.color is None:
            empty_color_floors.append(floor)
        if floor.animal is None:
            empty_animal_floors.append(floor)

    if len(empty_color_floors) == 1 and len(unused_colors) == 1:
        empty_color_floors[0].color = unused_colors[0]
    if len(empty_animal_floors) == 1 and len(unused_animals) == 1:
        empty_animal_floors[0].animal = unused_animals[0]


def complete_last_available_absolute_color_animal_hint(
    tower: dict[Floor, PicassoTowerFloor], color: Color, animal: Animal
) -> None:
    """
    In cases where there is only one empty floor and an absolute hint was given connecting a color and animal,
    this function responsible for inserting those color and animal to the last empty floor.
    """
    empty_floors = []

    for floor in tower.values():
        if floor.color is None and floor.animal is None:
            empty_floors.append(floor)

    if len(empty_floors) == 1:
        empty_floors[0].color = color
        empty_floors[0].animal = animal

from pydantic import BaseModel
from picasso_tower.models import Animal, Color, Floor


class PicassoTowerFloor(BaseModel):
    animal: Animal | None
    color: Color | None


class PicassoTower:
    def __init__(self, floors_number: int):
        self.floors: dict[Floor, PicassoTowerFloor] = {Floor(i + 1): PicassoTowerFloor() for i in range(floors_number)}


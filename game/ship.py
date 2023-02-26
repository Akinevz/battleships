from __future__ import annotations

ship_character = '.'
sunken_ship_character = 'x'
missed_shot_character = 'o'


class Ship:
    def __init__(self, origin: tuple[int, int], length: int, orientation: str):
        self.length = length
        self.orientation = orientation
        self.pieces = make_ship_parts(origin, length, orientation)
        assert (len(self.pieces) == length)

    def hit(self, x: int, y: int) -> None:
        self.pieces[(x, y)] = SunkenShipPart()

    def sunk(self) -> bool:
        for (piece) in self.pieces.values():
            if (type(piece) is ShipPart):
                return False
        return True


class ShipPart:
    def __init__(self):
        self.fill = ship_character


class SunkenShipPart:
    def __init__(self):
        self.fill = sunken_ship_character


class MissedShot:
    def __init__(self):
        self.fill = missed_shot_character


def make_ship_parts(origin: tuple[int, int], length: int, orientation: str) -> dict[tuple[int, int], ShipPart]:
    if (orientation == 'h'):
        (x, y) = origin
        return {(x, y): ShipPart() for x in range(x, x+length)}
    if (orientation == 'v'):
        (x, y) = origin
        return {(x, y): ShipPart() for y in range(y, y+length)}

    raise ValueError("orientation must be 'v' or 'h'")

from __future__ import annotations
from typing import Union
from game.ship import Ship, ShipPart, SunkenShipPart, MissedShot, ship_character, sunken_ship_character
from io import StringIO

size_default = 12
playable_pieces = [6, 4, 4, 2, 1]


class OutOfBoundsError(ValueError):
    def __init__(self, point: tuple[int, int]) -> None:
        super().__init__(f"{point} is out of bounds")


class BoardCell:
    def __init__(self, content: Union[ShipPart, SunkenShipPart, MissedShot, None] = None):
        self.content = content

    def set(self, content: Union[ShipPart, SunkenShipPart, MissedShot]) -> None:
        self.content = content

    def show(self, reveal: bool) -> str:
        if (not reveal and type(self.content) is ShipPart):
            return " "
        return str(self)

    def miss(self) -> bool:
        return ((self.content) is None)

    def __str__(self) -> str:
        if (type(self.content) is SunkenShipPart):
            return self.content.fill
        if (type(self.content) is ShipPart):
            return self.content.fill
        if (type(self.content) is MissedShot):
            return self.content.fill
        return " "


class Board:
    def __init__(self, dimensions: int):
        self.pieces = [[BoardCell() for _ in range(dimensions)]
                       for _ in range(dimensions)]
        self.dimensions = (dimensions, dimensions)
        self.ships: dict[tuple[int, int], Ship] = {}

    # discuss board dimensions and doubly-nested lists
    def show_board(self, reveal: bool = False) -> str:
        """display the contents of the board"""
        buffer = pretty_print_board(self, reveal)
        return buffer

    def all_sunk(self) -> bool:
        for (ship) in self.ships.values():
            if not ship.sunk():
                return False
        return True

    # why does a try-method return a boolean?
    def try_attack(self, point: tuple[int, int]) -> bool:
        """returns True if a ship part was hit, False otherwise. raises an exception if point is out of bounds"""
        if (not self.contains(point)):
            raise OutOfBoundsError(point)

        (x, y) = point
        square = self.pieces[y][x]
        if (square.miss()):
            return self.mark_missed(x, y)
        if (type(square.content) == ShipPart):
            return self.mark_hit(x, y)
        return False

    def mark_hit(self, x: int, y: int) -> bool:
        sunken = SunkenShipPart()
        self.put(x, y, sunken)
        self.ships[(x, y)].hit(x, y)
        return True

    def mark_missed(self, x: int, y: int) -> bool:
        missed = MissedShot()
        self.put(x, y, missed)
        return False

    # what is a union type
    def put(self, x: int, y: int, data: Union[ShipPart, MissedShot, SunkenShipPart, None]) -> None:
        self.pieces[y][x].set(data)

    # what is the runtime complexity of this function
    def add_ship(self, piece: Ship) -> bool:
        for (point) in piece.pieces.keys():
            if (not self.free(point)):
                return False
        for (point, part) in piece.pieces.items():
            x, y = point
            self.put(x, y, part)
        for point in piece.pieces.keys():
            self.ships[point] = piece
        return True

    def contains(self, point: tuple[int, int]) -> bool:
        (x, y) = point
        return self.y_fits(y) and self.x_fits(x)

    # what is a Null type
    def free(self, point: tuple[int, int]) -> bool:
        (x, y) = point
        return self.pieces[y][x].content is None

    def y_fits(self, y: int) -> bool:
        (_, height) = self.dimensions
        return y >= 0 and y < height

    def x_fits(self, x: int) -> bool:
        (width, _) = self.dimensions
        return x >= 0 and x < width


# what are helper methods
def pretty_print_board(board: Board, reveal: bool) -> str:
    buffer = buffer_new()
    rownum = 1
    for row in board.pieces:
        rownum = print_row_str(buffer, rownum)
        for data in row:
            print_cel_str(buffer, data, reveal)
        print(file=buffer)
    print_col_str(buffer, len(board.pieces))
    print(file=buffer)
    return buffer.getvalue()


def print_cel_str(buffer: StringIO, data: BoardCell, reveal: bool) -> None:
    printable = data.show(reveal)
    print(f"[{printable}]", file=buffer, end='')


def print_col_str(buffer: StringIO, count: int) -> None:
    print(" "*2, file=buffer, end='')
    for colnum in range(count):
        colnum = f"{colnum+1}"
        print(colnum.rjust(3), file=buffer, end='')


def print_row_str(buffer: StringIO, rownum: int) -> int:
    rowstr = f"{rownum}"
    print(rowstr.rjust(3), file=buffer, end='')
    return rownum+1


# what is a buffer
def buffer_new() -> StringIO:
    return StringIO()

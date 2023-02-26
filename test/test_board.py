import unittest

from game.board import *


class TestBoardMethods(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.ships = [
            Ship((0, 0), 5, 'h'),
            Ship((0, 1), 5, 'h'),
            Ship((0, 2), 5, 'h'),
            Ship((0, 4), 5, 'h'),
        ]

    def test_create(self):
        board = Board(5)
        for ship in self.ships:
            board.add_ship(ship)
        print(board.show_board(True))
        for y in range(0, 5):
            for i in range(5):
                res = board.try_attack((i, y))
                print(str(res) + "\n" + board.show_board(True))
        print(board.all_sunk())
        print([ship.sunk() for ship in board.ships.values()])

        self.assertTrue(board.all_sunk())

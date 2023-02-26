from __future__ import annotations
from game.board import Board
from game.user import clear_screen, pause_for_input


class Player:
    def __init__(self, name: str):
        self.name = name
        self.won = False
        self.defeated = False
        self.board = None

    def set_board(self, board: Board) -> None:
        self.board = board

    def validate_turn(self, board: Board, point: tuple[int, int]) -> bool:
        return (board.contains(point))

    def hit(self, board: Board) -> bool:
        print("Where do you attack? (x): ", end='')
        x = int(input())-1
        print()

        print("Where do you attack? (y): ", end='')
        y = int(input())-1

        if (self.validate_turn(board, (x, y))):
            return self.attack(board, (x, y))
        raise ValueError("That's not a valid coordinate!")

    def attack(self, board: Board, point: tuple[int, int]) -> bool:
        return board.try_attack(point)

    def play_round(self, opponent: Board) -> None:
        pause_for_input()
        clear_screen()
        print(f"{self.name}'s turn!")
        print("Enemy board looks like this:")
        print(opponent.show_board())
        try:
            hit = self.hit(opponent)
            print("That's a hit!" if hit else "That's a miss!")
        except ValueError:
            print("That doesn't seem right...")
            self.play_round(opponent)
        except EOFError as ex:
            print("Interrupt received: "+str(ex))
            return

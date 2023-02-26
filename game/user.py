from __future__ import annotations
import os
from game.board import Board
from game.ship import Ship


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause_for_input() -> None:
    try:
        input("Press enter to continue: ")
    except:
        pass



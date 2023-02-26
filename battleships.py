from __future__ import annotations

from game.board import Board, size_default, playable_pieces
from game.ship import Ship
from game.player import Player
from game.user import clear_screen, pause_for_input

WELCOME_TEXT = "Hello and welcome to Battleships!"
PLAYER_START = "Player {number}, please state your name: "


def main():
    names = introduce()
    player1, player2 = start(names)
    if (player1.won):
        congratulate(player1)
    if (player2.won):
        congratulate(player2)
    print("End of game")


def introduce() -> tuple[str, str]:
    print(WELCOME_TEXT)
    name1 = ""
    name2 = ""
    try:
        print(PLAYER_START.format(number=1))
        name1 = input()
        print(PLAYER_START.format(number=2))
        name2 = input()
    except EOFError:
        clear_screen()
        return introduce()

    return (name1, name2)


def players(names: tuple[str, str]) -> tuple[Player, Player]:
    return (Player(name) for name in names)


def start(names: tuple[str, str]) -> tuple[Player, Player]:
    board1 = Board(size_default)
    board2 = Board(size_default)
    # analyse the code inside player.players()
    (player1, player2) = players(names)
    # what happens if we forget to call player.set_board()?
    player1.set_board(board1)
    player2.set_board(board2)

    setup_pieces(player1)
    setup_pieces(player2)

    play_round(1, players=(player1, player2))
    return (player1, player2)


def game_over(winner: Player) -> None:
    winner.won = True


def play_round(round: int, players: tuple[Player, Player]) -> None:
    (p1, p2) = players
    if (p1.defeated):
        return game_over(p2)
    if (p2.defeated):
        return game_over(p1)

    player = p2 if round % 2 == 0 else p1
    opponent = p2 if round % 2 == 1 else p1

    player.play_round(opponent.board)
    if (opponent.board.all_sunk()):
        opponent.defeated = True
    play_round(round=round+1, players=players)


def prompt_setup(player: str, board: Board, length: int) -> None:
    pause_for_input()
    clear_screen()
    print(f"Player {player} is setting up their board:")
    print("The board looks like this:")
    print(board.show_board(reveal=True))
    try:
        x = int(input(f"Enter (x) of Piece({length}): "))-1
        y = int(input(f"Enter (y) of Piece({length}): "))-1
        orientation = str(input(f"Enter orientation (h/v): "))
        ship = Ship((x, y), length, orientation)
        if (not board.add_ship(ship)):
            print("That ship doesn't fit, try again")
            prompt_setup(player, board, length)
    except ValueError as ve:
        print("Error: "+str(ve))
        prompt_setup(player, board, length)
    except EOFError as eof:
        print("Resetting current piece")
        prompt_setup(player, board, length)
        return


def setup_pieces(player: Player) -> None:
    for piece in playable_pieces:
        prompt_setup(player.name, player.board, piece)


def congratulate(player: Player) -> None:
    print(f"{player.name} wins!")


if __name__ == "__main__":
    main()

from game import Game
from ui import UI


def main():
    start_budget = 100000
    city_name = "Monorail City"

    game = Game(start_budget, city_name)
    ui = UI(game)
    ui.start_game()


if __name__ == "__main__":
    main()

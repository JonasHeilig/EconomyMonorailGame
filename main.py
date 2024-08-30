from game import Game
from ui import UI
import tkinter as tk


def main():
    start_budget = 100000
    city_name = "Monorail City"

    game = Game(start_budget, city_name)
    root = tk.Tk()
    ui = UI(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()

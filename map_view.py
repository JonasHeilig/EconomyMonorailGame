import tkinter as tk

class MapView:
    def __init__(self, root, map_data, game):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack()
        self.game = game

        for station_name, coords in map_data.items():
            self.canvas.create_oval(coords[0] - 10, coords[1] - 10, coords[0] + 10, coords[1] + 10, fill="blue")
            self.canvas.create_text(coords[0], coords[1] - 15, text=station_name)

        self.root.mainloop()

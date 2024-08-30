import tkinter as tk
from tkinter import messagebox
from game import Game, Train, Bus, Tram, Inspector, Level
from map_view import MapView

class UI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title(f"Monorail Manager Game - {self.game.city_name}")
        self.root.geometry("600x600")
        self.update_ui()

    def start_game(self):
        self.root.mainloop()

    def update_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        status = self.game.show_status()
        self.create_header(status)
        self.create_vehicle_buttons()
        self.create_level_buttons()
        self.create_management_buttons()
        self.create_map_button()

    def create_header(self, status):
        header_frame = tk.Frame(self.root, bg="lightblue")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text=f"Stadt: {status['Stadt']}", font=("Arial", 14, "bold"), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Budget: {status['Budget']} €", font=("Arial", 12), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Züge: {len(self.game.trains)}", font=("Arial", 12), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Busse: {len(self.game.buses)}", font=("Arial", 12), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Straßenbahnen: {len(self.game.trams)}", font=("Arial", 12), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Schienen: {self.game.tracks}", font=("Arial", 12), bg="lightblue").pack(pady=5)
        tk.Label(header_frame, text=f"Kontrolleur-Stufe: {status['Kontrolleur-Stufe']}", font=("Arial", 12), bg="lightblue").pack(pady=5)

    def create_vehicle_buttons(self):
        vehicle_frame = tk.Frame(self.root, bg="lightgrey")
        vehicle_frame.pack(pady=10)
        tk.Label(vehicle_frame, text="Verfügbare Fahrzeuge:", font=("Arial", 12, "bold"), bg="lightgrey").pack()
        if "Straßenbahnen" in self.game.available_transport:
            tk.Button(vehicle_frame, text="Neue Straßenbahn kaufen", command=self.add_tram, width=30).pack(pady=5)
        if "Busse" in self.game.available_transport:
            tk.Button(vehicle_frame, text="Neuen Bus kaufen", command=self.add_bus, width=30).pack(pady=5)
        if "Züge" in self.game.available_transport:
            tk.Button(vehicle_frame, text="Neuen Zug kaufen", command=self.add_train, width=30).pack(pady=5)
        tk.Button(vehicle_frame, text="Schienen bauen", command=self.build_tracks, width=30).pack(pady=5)

    def create_level_buttons(self):
        level_frame = tk.Frame(self.root, bg="lightyellow")
        level_frame.pack(pady=10)
        tk.Label(level_frame, text="Levels kaufen:", font=("Arial", 12, "bold"), bg="lightyellow").pack()
        for level in self.game.levels:
            tk.Button(level_frame, text=f"{level.name} - {level.cost} €",
                      command=lambda l=level: self.buy_level(l), width=30).pack(pady=5)

    def create_management_buttons(self):
        management_frame = tk.Frame(self.root, bg="lightgreen")
        management_frame.pack(pady=10)
        tk.Button(management_frame, text="Kontrolleur einstellen", command=self.hire_inspector, width=30).pack(pady=5)
        tk.Button(management_frame, text="Upgrade Fahrzeuge", command=self.upgrade_vehicles, width=30).pack(pady=5)
        tk.Button(management_frame, text="Nächste Runde", command=self.manage_turn, width=30).pack(pady=5)

    def create_map_button(self):
        tk.Button(self.root, text="Karte anzeigen", command=self.show_map, width=30).pack(pady=10)

    def add_train(self):
        result = self.game.add_train()
        messagebox.showinfo("Info", result)
        self.update_ui()

    def add_bus(self):
        result = self.game.add_bus()
        messagebox.showinfo("Info", result)
        self.update_ui()

    def add_tram(self):
        result = self.game.add_tram()
        messagebox.showinfo("Info", result)
        self.update_ui()

    def build_tracks(self):
        result = self.game.build_tracks()
        messagebox.showinfo("Info", result)
        self.update_ui()

    def buy_level(self, level):
        result = self.game.buy_level(level)
        messagebox.showinfo("Level Kauf", result)
        self.update_ui()

    def hire_inspector(self):
        result = self.game.hire_inspector()
        messagebox.showinfo("Kontrolleur", result)
        self.update_ui()

    def upgrade_vehicles(self):
        def upgrade(vehicle):
            result = self.game.upgrade_vehicle(vehicle)
            messagebox.showinfo("Upgrade", result)
            self.update_ui()

        upgrade_frame = tk.Toplevel(self.root)
        upgrade_frame.title("Fahrzeug Upgrades")
        tk.Label(upgrade_frame, text="Wählen Sie ein Fahrzeug zum Upgraden:", font=("Arial", 12, "bold")).pack(pady=10)

        for vehicle_list in [self.game.trains, self.game.buses, self.game.trams]:
            for vehicle in vehicle_list:
                tk.Button(upgrade_frame, text=f"Upgrade {vehicle.name}", command=lambda v=vehicle: upgrade(v)).pack(pady=5)

    def manage_turn(self):
        event, result, message = self.game.manage_turn()
        messagebox.showinfo("Ereignis", f"{event}\n{message}")
        if result:
            messagebox.showinfo("Info", result)
        self.update_ui()

    def show_map(self):
        map_window = tk.Toplevel(self.root)
        map_window.title("Kartenansicht")
        map_data = {station.name: (i * 50 + 50, 100) for i, station in enumerate(self.game.stations)}
        MapView(map_window, map_data)

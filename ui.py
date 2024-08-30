import tkinter as tk
from tkinter import messagebox
from game import Game
from map_view import MapView


class UI:
    def __init__(self, root):
        self.root = root
        self.game = Game(start_budget=100000, city_name="Berlin")
        self.root.title(f"Monorail Manager Game - {self.game.city_name}")

        self.status_label = tk.Label(root, text=self.get_status_text(), justify=tk.LEFT)
        self.status_label.pack()

        self.add_train_button = tk.Button(root, text="Zug kaufen", command=self.add_train)
        self.add_train_button.pack()

        self.add_bus_button = tk.Button(root, text="Bus kaufen", command=self.add_bus)
        self.add_bus_button.pack()

        self.add_tram_button = tk.Button(root, text="Straßenbahn kaufen", command=self.add_tram)
        self.add_tram_button.pack()

        self.build_tracks_button = tk.Button(root, text="Schienen bauen", command=self.build_tracks)
        self.build_tracks_button.pack()

        self.repair_vehicle_button = tk.Button(root, text="Fahrzeug reparieren", command=self.repair_vehicle)
        self.repair_vehicle_button.pack()

        self.maintenance_vehicle_button = tk.Button(root, text="Fahrzeug warten", command=self.maintenance_vehicle)
        self.maintenance_vehicle_button.pack()

        self.upgrade_vehicle_button = tk.Button(root, text="Fahrzeug upgraden", command=self.upgrade_vehicle)
        self.upgrade_vehicle_button.pack()

        self.inspect_button = tk.Button(root, text="Fahrgäste kontrollieren", command=self.inspect_vehicles)
        self.inspect_button.pack()

        self.next_turn_button = tk.Button(root, text="Nächste Runde", command=self.next_turn)
        self.next_turn_button.pack()

        self.map_button = tk.Button(root, text="Karte anzeigen", command=self.show_map)
        self.map_button.pack()

    def get_status_text(self):
        status = self.game.show_status()
        status_text = "\n".join([f"{key}: {value}" for key, value in status.items()])
        return status_text

    def refresh_status(self):
        self.status_label.config(text=self.get_status_text())

    def add_train(self):
        message = self.game.add_train()
        self.refresh_status()
        messagebox.showinfo("Zug gekauft", message)

    def add_bus(self):
        message = self.game.add_bus()
        self.refresh_status()
        messagebox.showinfo("Bus gekauft", message)

    def add_tram(self):
        message = self.game.add_tram()
        self.refresh_status()
        messagebox.showinfo("Straßenbahn gekauft", message)

    def build_tracks(self):
        message = self.game.build_tracks()
        self.refresh_status()
        messagebox.showinfo("Schienenbau", message)

    def repair_vehicle(self):
        vehicle = self.select_vehicle()
        if vehicle:
            message = self.game.repair_vehicle(vehicle)
            self.refresh_status()
            messagebox.showinfo("Reparatur", message)

    def maintenance_vehicle(self):
        vehicle = self.select_vehicle()
        if vehicle:
            message = self.game.maintenance_vehicle(vehicle)
            self.refresh_status()
            messagebox.showinfo("Wartung", message)

    def upgrade_vehicle(self):
        vehicle = self.select_vehicle()
        if vehicle:
            message = self.game.upgrade_vehicle(vehicle)
            self.refresh_status()
            messagebox.showinfo("Upgrade", message)

    def inspect_vehicles(self):
        message = self.game.inspect_vehicles()
        self.refresh_status()
        messagebox.showinfo("Inspektion", message)

    def next_turn(self):
        event, effect = self.game.manage_turn()
        self.refresh_status()
        messagebox.showinfo("Nächste Runde", f"{event}\n{effect}")

    def show_map(self):
        map_window = tk.Toplevel(self.root)
        map_window.title("Kartenansicht")
        map_data = {station.name: (i * 50 + 50, 100) for i, station in enumerate(self.game.stations)}
        MapView(map_window, map_data, self.game)

    def select_vehicle(self):
        vehicles = self.game.trains + self.game.buses + self.game.trams
        if not vehicles:
            messagebox.showwarning("Keine Fahrzeuge", "Es gibt keine Fahrzeuge zur Auswahl.")
            return None
        vehicle_names = [vehicle.name for vehicle in vehicles]
        selected_vehicle_name = tk.simpledialog.askstring("Fahrzeug auswählen",
                                                          f"Wähle ein Fahrzeug aus: {', '.join(vehicle_names)}")
        selected_vehicle = next((v for v in vehicles if v.name == selected_vehicle_name), None)
        if not selected_vehicle:
            messagebox.showwarning("Ungültige Auswahl", "Fahrzeug nicht gefunden.")
        return selected_vehicle


if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()

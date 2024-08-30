import tkinter as tk
from tkinter import messagebox, simpledialog
from game import Game
from map_view import MapView


class UI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title(f"Monorail Manager Game - {self.game.city_name}")
        self.root.geometry("350x700")

        self.status_label = tk.Label(root, text=self.get_status_text(), justify=tk.LEFT, font=("Helvetica", 12))
        self.status_label.pack(padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.create_button(button_frame, "Zug kaufen", self.add_train)
        self.create_button(button_frame, "Bus kaufen", self.add_bus)
        self.create_button(button_frame, "Straßenbahn kaufen", self.add_tram)
        self.create_button(button_frame, "Schienen bauen", self.build_tracks)
        self.create_button(button_frame, "Fahrzeug reparieren", self.repair_vehicle)
        self.create_button(button_frame, "Fahrzeug warten", self.maintenance_vehicle)
        self.create_button(button_frame, "Fahrzeug upgraden", self.upgrade_vehicle)
        self.create_button(button_frame, "Fahrgäste kontrollieren", self.inspect_vehicles)
        self.create_button(button_frame, "Nächste Runde", self.next_turn)
        self.create_button(button_frame, "Karte anzeigen", self.show_map)

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, width=20, height=2, font=("Helvetica", 10))
        button.pack(pady=5)

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
        selected_vehicle_name = simpledialog.askstring("Fahrzeug auswählen",
                                                       f"Wähle ein Fahrzeug aus: {', '.join(vehicle_names)}")
        if not selected_vehicle_name:
            return None
        selected_vehicle = next((v for v in vehicles if v.name == selected_vehicle_name), None)
        if not selected_vehicle:
            messagebox.showwarning("Ungültige Auswahl", "Fahrzeug nicht gefunden.")
        return selected_vehicle


if __name__ == "__main__":
    root = tk.Tk()
    game_instance = Game(start_budget=100000, city_name="Berlin")
    app = UI(root, game_instance)
    root.mainloop()

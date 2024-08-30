import random

class Passenger:
    def __init__(self, destination):
        self.destination = destination
        self.has_ticket = random.choice([True, False])

class Station:
    def __init__(self, name):
        self.name = name
        self.passengers = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

    def waiting_passengers(self):
        return len(self.passengers)

class Vehicle:
    def __init__(self, name, capacity=30, upgrade_cost=10000):
        self.name = name
        self.passengers = []
        self.capacity = capacity
        self.upgrade_cost = upgrade_cost
        self.defekt = False
        self.wartungsbedarf = False
        self.upgrade_stufe = 0

    def repair(self):
        if self.defekt:
            self.defekt = False
            return f"{self.name} wurde repariert."
        else:
            return f"{self.name} ist nicht defekt."

    def maintenance(self):
        if self.wartungsbedarf:
            self.wartungsbedarf = False
            return f"Wartung von {self.name} abgeschlossen."
        else:
            return f"{self.name} benötigt keine Wartung."

    def upgrade(self):
        if self.upgrade_stufe < 3:
            self.upgrade_stufe += 1
            self.capacity = int(self.capacity * 1.2)  # Kapazität erhöhen
            return f"{self.name} wurde auf Stufe {self.upgrade_stufe} upgegraded."
        else:
            return f"{self.name} ist bereits auf maximalem Upgrade-Level."

    def board_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return f"Passagier in {self.name} eingestiegen."
        else:
            return f"{self.name} ist voll!"

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

class Train(Vehicle):
    def __init__(self, name):
        super().__init__(name, upgrade_cost=20000)

class Bus(Vehicle):
    def __init__(self, name):
        super().__init__(name, upgrade_cost=15000)

class Tram(Vehicle):
    def __init__(self, name):
        super().__init__(name, upgrade_cost=25000)

class Inspector:
    def __init__(self):
        self.caught_fare_dodgers = 0
        self.fine_per_dodger = 50

    def check_passengers(self, vehicle):
        fare_dodgers = [p for p in vehicle.passengers if not p.has_ticket]
        self.caught_fare_dodgers += len(fare_dodgers)
        for passenger in fare_dodgers:
            vehicle.remove_passenger(passenger)
        if fare_dodgers:
            fine_total = len(fare_dodgers) * self.fine_per_dodger
            return f"Schwarzfahrer erwischt! {vehicle.name} schmeißt {len(fare_dodgers)} Passagiere raus. Bußgeld: {fine_total} €."
        else:
            return "Keine Schwarzfahrer entdeckt."

class Game:
    def __init__(self, start_budget, city_name):
        self.budget = start_budget
        self.city_name = city_name
        self.trains = []
        self.buses = []
        self.trams = []
        self.stations = [Station("Hauptbahnhof")]
        self.available_transport = []
        self.repair_cost = 7000
        self.new_train_cost = 30000
        self.new_bus_cost = 15000
        self.new_tram_cost = 40000
        self.new_station_cost = 20000
        self.tracks = 0
        self.inspector_level = 0
        self.inspector = Inspector()

    def add_train(self):
        if self.budget >= self.new_train_cost:
            train_name = f"Train {len(self.trains) + 1}"
            self.trains.append(Train(train_name))
            self.budget -= self.new_train_cost
            return f"Zug {train_name} wurde gekauft."
        else:
            return "Nicht genügend Budget, um einen neuen Zug zu kaufen."

    def add_bus(self):
        if self.budget >= self.new_bus_cost:
            bus_name = f"Bus {len(self.buses) + 1}"
            self.buses.append(Bus(bus_name))
            self.budget -= self.new_bus_cost
            return f"Bus {bus_name} wurde gekauft."
        else:
            return "Nicht genügend Budget, um einen neuen Bus zu kaufen."

    def add_tram(self):
        if self.budget >= self.new_tram_cost:
            tram_name = f"Tram {len(self.trams) + 1}"
            self.trams.append(Tram(tram_name))
            self.budget -= self.new_tram_cost
            return f"Straßenbahn {tram_name} wurde gekauft."
        else:
            return "Nicht genügend Budget, um eine neue Straßenbahn zu kaufen."

    def repair_vehicle(self, vehicle):
        if self.budget >= self.repair_cost:
            self.budget -= self.repair_cost
            return vehicle.repair()
        else:
            return "Nicht genügend Budget für die Reparatur."

    def maintenance_vehicle(self, vehicle):
        if self.budget >= self.repair_cost:
            self.budget -= self.repair_cost
            return vehicle.maintenance()
        else:
            return "Nicht genügend Budget für die Wartung."

    def upgrade_vehicle(self, vehicle):
        if self.budget >= vehicle.upgrade_cost:
            self.budget -= vehicle.upgrade_cost
            return vehicle.upgrade()
        else:
            return "Nicht genügend Budget für das Upgrade."

    def inspect_vehicles(self):
        total_fine = 0
        for train in self.trains:
            message = self.inspector.check_passengers(train)
            if "Bußgeld" in message:
                total_fine += int(message.split()[-2].replace("€", ""))
        for bus in self.buses:
            message = self.inspector.check_passengers(bus)
            if "Bußgeld" in message:
                total_fine += int(message.split()[-2].replace("€", ""))
        for tram in self.trams:
            message = self.inspector.check_passengers(tram)
            if "Bußgeld" in message:
                total_fine += int(message.split()[-2].replace("€", ""))
        self.budget += total_fine
        return f"Inspektion abgeschlossen. Gesamtes Bußgeld: {total_fine} €."

    def build_tracks(self):
        if self.budget >= 75000:
            self.tracks += 1
            self.budget -= 75000
            return "Neue Schienen wurden gebaut."
        else:
            return "Nicht genügend Budget zum Bau neuer Schienen."

    def show_status(self):
        return {
            "Stadt": self.city_name,
            "Budget": self.budget,
            "Züge": len(self.trains),
            "Busse": len(self.buses),
            "Straßenbahnen": len(self.trams),
            "Schienen": self.tracks
        }

    def manage_turn(self):
        event = random.choice([
            "Ein Zug ist defekt",
            "Wartungsbedarf für einen Bus",
            "Straßenbahn hat Verspätung"
        ])
        effect = self.handle_event(event)
        return event, effect

    def handle_event(self, event):
        if event == "Ein Zug ist defekt" and self.trains:
            train = random.choice(self.trains)
            train.defekt = True
            return f"{train.name} ist defekt."
        elif event == "Wartungsbedarf für einen Bus" and self.buses:
            bus = random.choice(self.buses)
            bus.wartungsbedarf = True
            return f"{bus.name} benötigt Wartung."
        elif event == "Straßenbahn hat Verspätung" and self.trams:
            tram = random.choice(self.trams)
            tram.wartungsbedarf = True
            return f"{tram.name} hat Verspätung."
        return "Keine besonderen Ereignisse."

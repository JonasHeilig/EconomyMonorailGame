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
            self.upgrade_cost *= 1.5
            return f"{self.name} wurde auf Stufe {self.upgrade_stufe} upgegraded."
        else:
            return f"{self.name} ist bereits auf maximalem Upgrade-Level."

    def board_passenger(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return f"Passagier in {self.name} eingestiegen."
        else:
            return f"{self.name} ist voll!"

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

    def check_passengers(self, vehicle):
        fare_dodgers = [p for p in vehicle.passengers if not p.has_ticket]
        self.caught_fare_dodgers += len(fare_dodgers)
        for passenger in fare_dodgers:
            vehicle.remove_passenger(passenger)
        if fare_dodgers:
            return f"Schwarzfahrer erwischt! {vehicle.name} schmeißt {len(fare_dodgers)} Passagiere raus."
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
        self.levels = [
            Level("Stufe 1: Straßenbahnen", 60000, ["Straßenbahnen"]),
            Level("Stufe 2: Busse", 120000, ["Busse"]),
            Level("Stufe 3: Züge", 240000, ["Züge"])
        ]
        self.available_transport = []
        self.repair_cost = 7000
        self.new_train_cost = 30000
        self.new_bus_cost = 15000
        self.new_tram_cost = 40000
        self.tracks = 0
        self.inspector_level = 0

    def add_train(self):
        if self.budget >= self.new_train_cost:
            train_name = f"Train-{len(self.trains) + 1}"
            self.trains.append(Train(train_name))
            self.budget -= self.new_train_cost
            return f"Ein neuer Zug ({train_name}) wurde hinzugefügt."
        else:
            return "Nicht genügend Budget für einen neuen Zug."

    def add_bus(self):
        if self.budget >= self.new_bus_cost:
            bus_name = f"Bus-{len(self.buses) + 1}"
            self.buses.append(Bus(bus_name))
            self.budget -= self.new_bus_cost
            return f"Ein neuer Bus ({bus_name}) wurde hinzugefügt."
        else:
            return "Nicht genügend Budget für einen neuen Bus."

    def add_tram(self):
        if self.budget >= self.new_tram_cost:
            tram_name = f"Tram-{len(self.trams) + 1}"
            self.trams.append(Tram(tram_name))
            self.budget -= self.new_tram_cost
            return f"Eine neue Straßenbahn ({tram_name}) wurde hinzugefügt."
        else:
            return "Nicht genügend Budget für eine neue Straßenbahn."

    def repair_vehicle(self, vehicle):
        if self.budget >= self.repair_cost:
            self.budget -= self.repair_cost
            return vehicle.repair()
        else:
            return "Nicht genügend Budget für Reparaturen."

    def maintenance_vehicle(self, vehicle):
        if self.budget >= self.repair_cost:
            self.budget -= self.repair_cost
            return vehicle.maintenance()
        else:
            return "Nicht genügend Budget für Wartung."

    def upgrade_vehicle(self, vehicle):
        if self.budget >= vehicle.upgrade_cost:
            self.budget -= vehicle.upgrade_cost
            return vehicle.upgrade()
        else:
            return "Nicht genügend Budget für ein Upgrade."

    def build_tracks(self):
        if self.budget >= 75000:
            self.tracks += 1
            self.budget -= 75000
            return "Schienen wurden gebaut."
        else:
            return "Nicht genügend Budget zum Bau von Schienen."

    def random_event(self):
        events = [
            {"event": "Viele Fahrgäste warten auf den Zug.", "effect": lambda: self.increase_revenue(30000)},
            {"event": "Ein Zug ist kaputt gegangen.", "effect": self.random_train_defect},
            {"event": "Eine Straße muss repariert werden.", "effect": lambda: self.decrease_budget(20000)},
            {"event": "Straßenbahn benötigt Wartung.", "effect": self.random_tram_maintenance}
        ]
        event = random.choice(events)
        effect_result = event["effect"]()
        return event["event"], effect_result

    def random_train_defect(self):
        if self.trains:
            train = random.choice(self.trains)
            train.defekt = True
            return f"{train.name} ist kaputt gegangen."
        else:
            return "Keine Züge vorhanden."

    def random_tram_maintenance(self):
        if self.trams:
            tram = random.choice(self.trams)
            tram.wartungsbedarf = True
            return f"{tram.name} benötigt Wartung."
        else:
            return "Keine Straßenbahnen vorhanden."

    def increase_revenue(self, amount):
        self.budget += amount

    def decrease_budget(self, amount):
        self.budget -= amount

    def show_status(self):
        status = {
            "Stadt": self.city_name,
            "Budget": self.budget,
            "Züge": len(self.trains),
            "Busse": len(self.buses),
            "Straßenbahnen": len(self.trams),
            "Schienen": self.tracks,
            "Kontrolleur-Stufe": self.inspector_level
        }
        return status

    def manage_turn(self):
        income = 20000 + (len(self.trains) * 2000 * sum(train.upgrade_stufe + 1 for train in self.trains))
        income += (len(self.buses) * 8000 * sum(bus.upgrade_stufe + 1 for bus in self.buses))
        income += (len(self.trams) * 12000 * sum(tram.upgrade_stufe + 1 for tram in self.trams))
        self.budget += income
        return self.random_event()

    def buy_level(self, level):
        if self.budget >= level.cost:
            self.budget -= level.cost
            self.available_transport.extend(level.unlocks)
            if "Busse" in level.unlocks:
                self.stations.append(Station("Bushaltestelle Ost"))
            if "Züge" in level.unlocks:
                self.stations.append(Station("Bahnhof West"))
            return f"{level.name} freigeschaltet!"
        else:
            return "Nicht genügend Budget, um dieses Level zu kaufen."

    def send_vehicle(self, vehicle, station):
        if station.waiting_passengers() > 0:
            while station.waiting_passengers() > 0 and len(vehicle.passengers) < vehicle.capacity:
                passenger = station.passengers[0]
                station.remove_passenger(passenger)
                vehicle.board_passenger(passenger)
            revenue = sum(1 for p in vehicle.passengers if p.has_ticket) * 10
            self.budget += revenue
            return f"{vehicle.name} hat {len(vehicle.passengers)} Passagiere an Bord genommen. Einnahmen: {revenue} €."
        else:
            return "Keine Passagiere an der Station."

class Level:
    def __init__(self, name, cost, unlocks):
        self.name = name
        self.cost = cost
        self.unlocks = unlocks

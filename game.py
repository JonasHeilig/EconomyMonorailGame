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
        super().__init__(name, upgrade_cost=15000)

class Bus(Vehicle):
    def __init__(self, name):
        super().__init__(name, upgrade_cost=10000)

class Tram(Vehicle):
    def __init__(self, name):
        super().__init__(name, upgrade_cost=20000)

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

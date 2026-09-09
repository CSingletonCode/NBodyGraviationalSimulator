import json
import os

from simulation.body import Body


class Sim_Manager:
    def __init__(self):
        self.bodies = []
        self.saved_simulation = "current_simulation.json"
        self.produce_simulation()

    def make_body(self, data):
        body = Body(data)
        self.bodies.append(body)

    def initialise_default(self):
        data = {
            "name": "The Sun",
            "type": "Star",
            "parent": None,
            "density": 1408.0,
            "radius": 696340.0,
            "spin": 600.0,
            "position": [0.0, 0.0, 0.0],
            "velocity": [0.0, 0.0, 0.0],
            "tilt": [0.0, 1.0, 0.0],
            "colour": [1.0, 0.5, 0.1],
        }
        self.make_body(data)
        data2 = {
            "name": "Test Body",
            "type": "Planet",
            "parent": "The Sun",
            "density": 5514.0,  # kg/m^3
            "radius": 69_911.0,  # Mean radius in km
            "spin": 23.93,
            "position": [149_597_870.0, 0.0, 0.0],  # 50 million km right (X)
            "velocity": [0.0, 0.0, 0.0],
            "tilt": [0.0, 1.0, 0.0],
            "colour": [1.0, 1.0, 1.0],
        }
        self.make_body(data2)


    def produce_simulation(self):
        if os.path.exists(self.saved_simulation):
            try:
                with open(self.saved_simulation, "r") as file:
                    save = json.load(file)
                    for data in save:
                        self.make_body(data)
            except Exception as e:
                self.initialise_default()
        else:
            self.initialise_default()

    def render(self, renderer):
        for body in self.bodies:
            body.draw(renderer)
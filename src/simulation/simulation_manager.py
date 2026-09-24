import json
import os
import numpy as np
from simulation.body import Body

class Sim_Manager:
    def __init__(self):
        self.bodies = []
        self.proportional_radius = False
        self.saved_simulation = "current_simulation.json"
        self.produce_simulation()

    def make_body(self, data):
        body = Body(data)
        self.bodies.append(body)



    def initialise_default(self):
        sun_data = {
            "name": "The Sun",
            "type": "Star",
            "parent": None,
            "density": 1408.0,
            "radius": 695700.0,
            "mass": 1.989e30,
            "r_period": 609.12,
            "spin": 2.865e-6,
            "position": np.array([0.0, 0.0, 0.0], dtype=np.float64),
            "velocity": np.array([0.0, 0.0, 0.0], dtype=np.float64),
            "tilt": np.array([0.1265, 0.0, 0.0], dtype=np.float64),
            "colour": np.array([1.0, 0.85, 0.3], dtype=np.float64),
        }
        self.make_body(sun_data)

    def toggle_proportional_radius(self):
        self.proportional_radius = not self.proportional_radius

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

    def render(self, renderer, paused, dt):
        renderer.proportional_radius = self.proportional_radius
        for body in self.bodies:
            if not paused:
                body.update_rotation(dt)
            body.draw(renderer)

    def save_simulation(self):
        all_data = [body.make_dict() for body in self.bodies]
        with open(self.saved_simulation, "w") as file:
            json.dump(all_data, file, indent=4)

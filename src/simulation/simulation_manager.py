import json
import os

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
            "density": 1408.0,  # kg/m^3
            "radius": 696340.0,  # km
            "spin": 609.0,  # km/s (equatorial surface rotational speed)
            "position": [0.0, 0.0, 0.0],  # km
            "velocity": [0.0, 0.0, 0.0],  # km/s
            "tilt": [0.02, 0.0, 0.0],  # degrees (solar axial tilt relative to ecliptic)
            "colour": [1.0, 0.85, 0.3],  # Warm yellow-white
        }
        self.make_body(sun_data)
        earth_data = {
            "name": "Earth",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 5514.0,  # kg/m^3
            "radius": 6371.0,  # km
            "spin": 23.93,  # km/s (equatorial surface rotational speed)
            "position": [149597870.0, 0.0, 0.0],  # km (1 AU at perihelion/mean)
            "velocity": [0.0, 29.78, 0.0],  # km/s (mean orbital speed)
            "tilt": [0.34, 0.0, 0.0],  # degrees (axial tilt)
            "colour": [0.2, 0.5, 0.9],  # Ocean blue
        }
        self.make_body(earth_data)
        jupiter_data = {
            "name": "Jupiter",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 1326.0,  # kg/m^3 (gas giant, less dense than Earth)
            "radius": 71492.0,  # km (equatorial radius)
            "spin": 9.93,  # km/s (equatorial surface speed from rapid 9.9-hr rotation)
            "position": [778570000.0, 0.0, 0.0],  # km (average distance from Sun ~5.2 AU)
            "velocity": [0.0, 13.1, 0.0],  # km/s (mean orbital speed)
            "tilt": [0.0, 0.0, 0.0],  # degrees (axial tilt)
            "colour": [0.85, 0.65, 0.4],  # Muted brownish-orange gas giant tone
        }
        self.make_body(jupiter_data)
        moon_data = {
            "name": "The Moon",
            "type": "Moon",
            "parent": "Earth",
            "density": 3344.0,  # kg/m^3 (rocky body)
            "radius": 1737.4,  # km
            "spin": 655.7,  # km/s (slow tidal-locked rotation)
            "position": [149982270.0, 0.0, 0.0],  # km (Earth's X position + 384,400 km Earth-Moon distance)
            "velocity": [0.0, 30.802, 0.0],  # km/s (Earth's orbital speed 29.78 + Moon's orbital speed 1.02)
            "tilt": [0.0, 0.0, 0.0],  # degrees (axial tilt)
            "colour": [0.7, 0.7, 0.7],  # Light grey
        }
        self.make_body(moon_data)

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
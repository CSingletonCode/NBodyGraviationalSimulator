import numpy as np

class Body:
    def __init__(self, data):
        self.name = data["name"]
        self.body_type = data["type"]
        self.parent = data["parent"]

        self.density = data["density"]
        self.radius = data["radius"]
        self.spin = data["spin"]

        self.position = np.array(data["position"], dtype=np.float64)
        self.velocity = np.array(data["velocity"], dtype=np.float64)
        self.tilt = np.array(data["tilt"], dtype=np.float64)
        self.colour = np.array(data["colour"], dtype=np.float64)

        self.mass = self.calculate_mass()

    def calculate_mass(self):
        volume = (4.0 / 3.0) * np.pi * ((self.radius * 1000.0) ** 3)
        mass = volume * self.density
        return mass

    def draw(self, renderer):
        renderer.draw(self)



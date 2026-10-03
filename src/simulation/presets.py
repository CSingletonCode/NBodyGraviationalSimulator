class Presets:
    """Values for some bodies in our solar system that can be easily added"""
    def __init__(self):
        self.preset_list = []
        self.sun_data = {
            "name": "The Sun",
            "type": "Star",
            "parent": None,
            "density": 1408.0, # kg/m3
            "radius": 695700.0, # km, to make writing them easier
            "mass": 1.98847e30, # kg
            "spin": 609.12, # Rotation period in hrs
            "position": [0.0, 0.0, 0.0], # km, relative to parent
            "velocity": [0.0, 0.0, 0.0], # km/s, relative to parent
            "tilt": [0.1262, 0.9920, 0.0], # normalised to be between -1 and 1
            "colour": [1.0, 0.85, 0.3], # normalised rgb values
        }
        self.preset_list.append(self.sun_data)

        self.mercury_data = {
            "name": "Mercury",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 5429.0,
            "radius": 2439.7,
            "mass": 3.3011e23,
            "spin": 1407.6,
            "position": [-19461023.3, 3679718.3, -66913625.9],
            "velocity": [45.7100, 5.7600, -13.2900],
            "tilt": [0.000593, 0.9999998, 0.0],
            "colour": [0.5, 0.5, 0.5],
        }
        self.preset_list.append(self.mercury_data)

        self.earth_data = {
            "name": "Earth",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 5513.0,
            "radius": 6371.0,
            "mass": 5.9722e24,
            "spin": 23.9345,
            "position": [-26503021.5, 0.0, 144693286.0],
            "velocity": [-29.79053, 0.0, -5.45664],
            "tilt": [0.39778, 0.91748, 0.0],
            "colour": [0.2, 0.5, 1.0],
        }
        self.preset_list.append(self.earth_data)

        self.moon_data = {
            "name": "The Moon",
            "type": "Moon",
            "parent": "Earth",
            "density": 3340.0,
            "radius": 1737.4,
            "mass": 7.342e22,
            "spin": -655.7,
            "position": [-291230.7, 32153.2, 235518.1],
            "velocity": [-0.66188, 0.08920, -0.72011],
            "tilt": [0.117, 0.99314, 0.0],
            "colour": [0.7, 0.7, 0.7],
        }
        self.preset_list.append(self.moon_data)

        self.mars_data = {
            "name": "Mars",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 3934.0,
            "radius": 3389.5,
            "mass": 6.4171e23,
            "spin": 24.6229,
            "position": [208034201.0, 5158245.0, -1959744.0],
            "velocity": [0.2270, -0.7812, 24.1200],
            "tilt": [0.42588, 0.90478, 0.0],
            "colour": [0.8, 0.3, 0.15],
        }
        self.preset_list.append(self.mars_data)

        self.jupiter_data = {
            "name": "Jupiter",
            "type": "Gas Giant",
            "parent": "The Sun",
            "density": 1326.0,
            "radius": 69911.0,
            "mass": 1.89813e27,
            "spin": 9.925,
            "position": [598137212.0, 12238269.0, 440775196.0],
            "velocity": [-7.9137, 0.1308, 11.1366],
            "tilt": [0.05464, 0.99851, 0.0],
            "colour": [0.8, 0.65, 0.4],
        }
        self.preset_list.append(self.jupiter_data)

        self.neptune_data = {
            "name": "Neptune",
            "type": "Ice Giant",
            "parent": "The Sun",
            "density": 1638.0,
            "radius": 24622.0,
            "mass": 1.02413e26,
            "spin": 16.11,
            "position": [2511411340.0, -19321584.0, -3748774410.0],
            "velocity": [4.5820, -0.1423, 3.0670],
            "tilt": [0.47495, 0.87977, 0.0],
            "colour": [0.2, 0.4, 0.9],
        }
        self.preset_list.append(self.neptune_data)

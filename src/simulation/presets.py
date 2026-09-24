class Presets:
    def __init__(self):
        self.preset_list = []
        sun_data = {
            "name": "The Sun",
            "type": "Star",
            "parent": None,
            "density": 1408.0,  # kg/m^3
            "radius": 695700.0,  # km (IAU nominal mean solar radius)
            "mass": 1.989e30,  # kg
            "r_period": 609.12,  # hours (~25.38 days rotation period)
            "spin": 609.12,  # km/s (equatorial surface rotational speed)
            "position": [0.0, 0.0, 0.0],  # km
            "velocity": [0.0, 0.0, 0.0],  # km/s
            "tilt": [0.1265, 0.0, 0.0],  # axial tilt in radians (7.25° converted to radians, between -1 and 1)
            "colour": [1.0, 0.85, 0.3],  # Normalized RGB
        }
        self.preset_list.append(sun_data)

        self.earth_data = {
            "name": "Earth",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 5513.0,
            "radius": 6371.0,
            "spin": 23.9345,
            "position": [-26503021.5, 144693286.0, 119.3],
            "velocity": [-29.7865, -5.4786, -0.00001],
            "tilt": [0.398, 0.0, 0.0],
            "colour": [0.2, 0.5, 1.0],
        }
        self.preset_list.append(self.earth_data)

        self.mercury_data = {
            "name": "Mercury",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 5429.0,
            "radius": 2439.7,
            "spin": 1407.6,
            "position": [-19461023.3, -66913625.9, -3679718.3],
            "velocity": [36.9950, -11.1642, -4.3076],
            "tilt": [0.001, 0.0, 0.0],
            "colour": [0.5, 0.5, 0.5],
        }
        self.preset_list.append(self.mercury_data)

        self.mars_data = {
            "name": "Mars",
            "type": "Terrestrial Planet",
            "parent": "The Sun",
            "density": 3934.0,
            "radius": 3389.5,
            "spin": 24.6229,
            "position": [208034201.0, -1959744.0, -5158245.0],
            "velocity": [1.1603, 26.2977, 0.5224],
            "tilt": [0.426, 0.0, 0.0],
            "colour": [0.8, 0.3, 0.15],
        }
        self.preset_list.append(self.mars_data)

        self.jupiter_data = {
            "name": "Jupiter",
            "type": "Gas Giant",
            "parent": "The Sun",
            "density": 1326.0,
            "radius": 69911.0,
            "spin": 9.925,
            "position": [598137212.0, 440775196.0, -15238269.0],
            "velocity": [-7.9137, 11.1366, 0.1308],
            "tilt": [0.054, 0.0, 0.0],
            "colour": [0.8, 0.65, 0.4],
        }
        self.preset_list.append(self.jupiter_data)

        self.neptune_data = {
            "name": "Neptune",
            "type": "Ice Giant",
            "parent": "The Sun",
            "density": 1638.0,
            "radius": 24764.0,
            "spin": 16.11,
            "position": [2511411340.0, -3748774410.0, 19321584.0],
            "velocity": [4.4717, 3.0555, -0.1660],
            "tilt": [0.474, 0.0, 0.0],
            "colour": [0.2, 0.4, 0.9],
        }
        self.preset_list.append(self.neptune_data)

        self.moon_data = {
            "name": "The Moon",
            "type": "Moon",
            "parent": "Earth",
            "density": 3340.0,
            "radius": 1737.4,
            "spin": 655.7,
            "position": [-293230.7, -269518.1, 35553.2],
            "velocity": [0.6338, -0.7449, -0.0082],
            "tilt": [0.117, 0.0, 0.0],
            "colour": [0.7, 0.7, 0.7],
        }
        self.preset_list.append(self.moon_data)

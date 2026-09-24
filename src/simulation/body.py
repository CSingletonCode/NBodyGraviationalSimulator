from collections import deque
import numpy as np
from pyglm import glm
from constants import RADIUS_SCALE, DISTANCE_SCALE, SIZE_CAPS


class Body:
    def __init__(self, data):
        self.name = data["name"]
        self.body_type = data["type"]
        self.parent = data["parent"]
        self.density = data["density"]
        self.radius = data["radius"]
        self.mass = data["mass"]
        self.r_period = data["r_period"]
        self.spin = data["spin"]
        self.position = np.asarray(data["position"], dtype=np.float64)
        self.velocity = np.asarray(data["velocity"], dtype=np.float64)
        self.tilt = np.asarray(data["tilt"], dtype=np.float64)
        self.colour = np.asarray(data["colour"], dtype=np.float64)
        self.rotation = 0.0

        self.trail = deque(maxlen=4000)
        self.trail_gap = (0.15 * DISTANCE_SCALE ) ** 2
        self.trail_on = False

    def make_dict(self):
        return {
            "name": self.name,
            "type": self.body_type,
            "parent": self.parent,
            "density": self.density,
            "radius": self.radius,
            "mass": self.mass,
            "r_period": self.r_period,
            "spin": self.spin,
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "tilt": self.tilt.tolist(),
            "colour": self.colour.tolist(),
            "rotation": self.rotation,
        }

    def update_rotation(self, dt):
        self.rotation =  (self.rotation + self.spin * dt) % (2.0 * np.pi)

    def get_model_matrix(self, proportional_radius):
        if proportional_radius:
            scaled_radius = self.radius / RADIUS_SCALE
        else:
            scaled_radius = max(self.radius / RADIUS_SCALE, SIZE_CAPS.get(self.body_type, 0.01))
        scaled_position = self.position / DISTANCE_SCALE

        model_matrix = glm.mat4(1.0)
        model_matrix = glm.translate(model_matrix, glm.vec3(*scaled_position)) # location

        final_pole = glm.normalize(glm.vec3(*self.tilt))
        tilt_rotation_axis = glm.cross(glm.vec3(0.0,1.0,0.0), final_pole)
        tilt_cos_angle = glm.dot(glm.vec3(0.0,1.0,0.0), final_pole)
        if glm.length(tilt_rotation_axis) > 1e-6:
            tilt_angle = glm.acos(tilt_cos_angle)
            model_matrix = glm.rotate(model_matrix, tilt_angle, glm.normalize(tilt_rotation_axis)) # tilt
        elif tilt_cos_angle < 0.0: # checks angle for a 180 flip
            model_matrix = glm.rotate(model_matrix, np.pi, glm.vec3(1.0, 0.0, 0.0))

        model_matrix = glm.rotate(model_matrix, self.rotation, glm.vec3(0.0, 1.0, 0.0)) # spin
        model_matrix = glm.scale(model_matrix, glm.vec3(scaled_radius, scaled_radius, scaled_radius)) # size

        return model_matrix

    def add_to_trail(self):
        if not self.trail:
            self.trail.append(self.position)
            return

        last_position = self.trail[-1]
        dx = last_position[0] - self.position[0]
        dy = last_position[1] - self.position[1]
        dz = last_position[2] - self.position[2]
        squared_dist = (dx * dx) + (dy * dy) + (dz * dz)

        if squared_dist >= self.trail_gap:
            self.trail.append(self.position)

    def toggle_trail(self):
        self.trail_on = not self.trail_on

    def clear_trail(self):
        self.trail.clear()

    def draw(self, renderer):
        renderer.draw(self)
        renderer.draw_trail(self)



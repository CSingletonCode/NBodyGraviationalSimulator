import numpy as np
from pyglm import glm
from constants import RADIUS_SCALE, DISTANCE_SCALE

class Body:
    def __init__(self, data):
        self.name = data["name"]
        self.body_type = data["type"]
        self.parent = data["parent"]

        self.density = data["density"]
        self.radius = data["radius"]
        self.r_period = data["spin"]
        self.spin = self.calculate_angular_velocity(data["spin"])

        self.position = self.calculate_world_position(data)
        self.velocity = self.calculate_world_velocity(data)
        self.tilt = np.array(data["tilt"], dtype=np.float64)
        self.colour = np.array(data["colour"], dtype=np.float64)

        self.rotation = 0.0
        self.mass = self.calculate_mass()

    def calculate_world_position(self, data):
        pos = np.array(data["position"], dtype=np.float64)
        if data["parent"] is not None and not isinstance(data["parent"], str):
            parent_pos = np.array(data["parent"].position, dtype=np.float64)
            pos += parent_pos
        return pos

    def calculate_world_velocity(self, data):
        vel = np.array(data["velocity"], dtype=np.float64)
        if data["parent"] is not None and not isinstance(data["parent"], str):
            parent_vel = np.array(data["parent"].velocity, dtype=np.float64)
            vel += parent_vel
        return vel

    def calculate_mass(self):
        volume = (4.0 / 3.0) * np.pi * ((self.radius * 1000.0) ** 3)
        mass = volume * self.density
        return mass

    def calculate_angular_velocity(self, rotation_period):
        v = ( 2.0 * np.pi ) / (3600.0 * rotation_period)
        return v

    def update_rotation(self, dt):
        self.rotation =  (self.rotation + self.spin * dt) % (2.0 * np.pi)

    def get_model_matrix(self):
        scaled_radius = self.radius / RADIUS_SCALE
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

    def draw(self, renderer):
        renderer.draw(self)



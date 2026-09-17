# VELOCITY VERLET INTEGRATION
# REPORT COLLISION AND PASS THROUGH

import numpy as np

class Physics_Engine():
    def __init__(self, bodies):
        self.bodies = bodies
        self.gravitational_constant = 6.6743e-11 #m3 kg-1 s-2
        self.softening_value =1e-3

    def calculate_acceleration(self, position_array, mass_array, dt):
        position_deltas = position_array[np.newaxis, :, :] - position_array[:, np.newaxis, :]
        squared_distance = np.sum(np.square(position_deltas), axis=2) + (self.softening_value**2)
        denominator = np.pow(squared_distance, -1.5)
        # Remove all diagonals to prevent bodies acting on themselves
        np.fill_diagonal(denominator, 0.0)
        main_fraction = denominator[:, :, np.newaxis] * mass_array[np.newaxis, :, np.newaxis]
        acceleration_array = self.gravitational_constant * np.sum(position_deltas * main_fraction, axis=1)
        return acceleration_array


    def calculate_position(self, current_position_array, current_velocity_array, current_acceleration_array, dt):
        new_position_array = current_position_array + current_velocity_array * dt + 0.5 * current_acceleration_array * dt**2
        return new_position_array

    def calculate_velocity(self, current_velocity_array, current_acceleration_array, new_acceleration_array, dt):
        average_acceleration = (current_acceleration_array + new_acceleration_array) * 0.5
        new_velocity_array = current_velocity_array + average_acceleration * dt
        return new_velocity_array

    def update_bodies(self, dt):
        if len(self.bodies) == 0:
            return

        # Get current positions, velocity and mass for every body in the simulation
        current_positions = np.array([body.position * 1000.0 for body in self.bodies], dtype=np.float64)
        current_velocity = np.array([body.velocity * 1000.0 for body in self.bodies], dtype=np.float64)
        masses = np.array([body.mass for body in self.bodies], dtype=np.float64)

        # Calculate acceleration
        current_acceleration = self.calculate_acceleration(current_positions, masses, dt)

        # Calculate new position
        new_positions = self.calculate_position(current_positions, current_velocity, current_acceleration, dt)

        # Calculate new acceleration
        new_acceleration = self.calculate_acceleration(new_positions, masses, dt)

        # Calculate new velocity
        new_velocity = self.calculate_velocity(current_velocity, current_acceleration, new_acceleration, dt)

        for i, body in enumerate(self.bodies):
            body.position = new_positions[i] /1000
            body.velocity = new_velocity[i] /1000
            print(body.position)
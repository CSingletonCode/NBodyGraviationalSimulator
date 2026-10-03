import numpy as np

class Physics_Engine():

    def __init__(self, bodies):
        self.bodies = bodies
        self.gravitational_constant = 6.6743e-11 #m3 kg-1 s-2
        self.softening_value = 1e-3

    def calculate_acceleration(self, position_array, mass_array, dt):
        """Calculates the acceleration of each body, based on the forces from every other body,
        uses the equation:
        a_i = G * Σ[j ≠ i] (m_j * (r_j - r_i)) / ((|r_j - r_i|² + ε²)^(3/2))
        Where:
        # a_i = acceleration of body i
        # G   = gravitational constant
        # m_j = mass of body j
        # r_i = position of body i
        # r_j = position of body j
        # ε   = softening value"""

        # Creates an (N, N, 3) array where each row contains the distance vectors from that body to every other body. Where N is the number of bodies
        position_deltas = position_array[np.newaxis, :, :] - position_array[:, np.newaxis, :]
        # Squares and sums each distance vector, adds a softening value to prevent 0 denominators and massive forces up close.
        squared_distance = np.sum(np.square(position_deltas), axis=2) + (self.softening_value**2)
        # Creates 1 / distance³ so
        denominator = np.pow(squared_distance, -1.5)
        # Remove all diagonals to prevent bodies acting on themselves
        np.fill_diagonal(denominator, 0.0)
        # Multiplies every denominator by the bodies mass, numpy turns the mass array from (N), to (1, N, 1) so it can be broadcast
        main_fraction = denominator[:, :, np.newaxis] * mass_array[np.newaxis, :, np.newaxis]
        # Multiplies the distances with the rest of the equation, sums them to get every force acting on each body, then multiplies by G.
        acceleration_array = self.gravitational_constant * np.sum(position_deltas * main_fraction, axis=1)
        return acceleration_array

    def calculate_position(self, current_position_array, current_velocity_array, current_acceleration_array, dt):
        """Calculates the equation:
        s_new = s_current + vt + (at²)/2
        To find the new position of every body."""
        new_position_array = current_position_array + current_velocity_array * dt + 0.5 * current_acceleration_array * dt**2
        return new_position_array

    def calculate_velocity(self, current_velocity_array, current_acceleration_array, new_acceleration_array, dt):
        """Estimates the velocity of every body using their average acceleration.
        Uses the equation:
        v = u + (a_old + a_new)t/2"""
        average_acceleration = (current_acceleration_array + new_acceleration_array) * 0.5
        new_velocity_array = current_velocity_array + average_acceleration * dt
        return new_velocity_array

    def update_bodies(self, dt, num_steps):
        """Uses Velocity verlet integration to calculate the forces, velocity, acceleration and positions of each body.
           Updates the positions and velocities of each body."""

        if len(self.bodies) == 0:
            return

        # Splits the time jump into smaller steps so accurate calculates can be performed at massive time scales.
        dt_step = dt / num_steps

        # Get current positions, velocity and mass for every body in the simulation
        current_positions = np.array([body.position * 1000.0 for body in self.bodies], dtype=np.float64)
        current_velocity = np.array([body.velocity * 1000.0 for body in self.bodies], dtype=np.float64)
        masses = np.array([body.mass for body in self.bodies], dtype=np.float64)

        # Runs as many times as the timescale is broken down into, more for larger times.
        for _ in range(num_steps):
            # Calculate acceleration
            current_acceleration = self.calculate_acceleration(current_positions, masses, dt_step)

            # Calculate new position
            new_positions = self.calculate_position(current_positions, current_velocity, current_acceleration, dt_step)

            # Calculate new acceleration
            new_acceleration = self.calculate_acceleration(new_positions, masses, dt_step)

            # Calculate new velocity
            new_velocity = self.calculate_velocity(current_velocity, current_acceleration, new_acceleration, dt_step)

            current_positions = new_positions
            current_velocity = new_velocity

        # Writes new positions to the body and checks if the trail can be updated.
        for i, body in enumerate(self.bodies):
            body.position = current_positions[i] / 1000.0
            body.velocity = current_velocity[i] / 1000.0
            body.add_to_trail()
from pyglm import glm
import math
import pygame as py
from constants import RADIUS_SCALE, DISTANCE_SCALE, SIZE_CAPS


class Camera:
    def __init__(self,screen_width, screen_height):
        self.current_target = glm.vec3(0.0, 0.0, 0.0) # Position the camera is centred on
        self.desired_target = glm.vec3(0.0, 0.0, 0.0) # Position the camera is moving to be centred on
        self.current_distance = 30 # Distance the screen is from the target in world units.
        self.desired_distance = 30 # Distance the screen should be from the target in world units.
        self.position = glm.vec3(0.0, 0.0, 30.0) # Position of the screen in world space
        self.slide_keys = {"w": False, "a": False,"s": False, "d": False}

        # Angles for the orientation of the camera
        self.pitch = glm.radians(0.0)
        self.yaw = glm.radians(90.0)

        self.fov = 45.0
        self.aspect_ratio = screen_width / screen_height
        # Boundaries for where bodies are rendered.
        self.near = 0.1
        self.far = 2000.0

        self.rotate_sensitivity = 0.0075
        self.slide_sensitivity = 1.75
        self.zoom_sensitivity = 1.0
        self.linear_interp_speed = 8.0 # How quickly the camera moves to its new location

        self.left_mouse_down = False
        self.locked_on = False
        self.locked_body = None

        self.proportional_radius = False

    def toggle_proportional_radius(self):
        self.proportional_radius = not self.proportional_radius

    def lock_on_body(self, body):
        """Centres the camera on the selected body, positions the camera at a distance proportional to the visual radius"""
        # Finds the visual size based on the radius setting and if the body has a cap.
        if not self.proportional_radius and body.body_type in SIZE_CAPS:
            active_radius = max(body.radius / RADIUS_SCALE, SIZE_CAPS.get(body.body_type))
        else:
            active_radius = body.radius / RADIUS_SCALE
        self.desired_target = glm.vec3(body.position) / DISTANCE_SCALE
        self.desired_distance = max(0.15, active_radius * 6.0) # Stops the camera from positioning closer than the render limit
        self.locked_body = body
        self.locked_on = True

    def zoom(self,offset):
        """Moves the camera forwards and backwards
           Holds the target as the focussed body if the cameras locked on,
           Moves the target with the camera if it's not."""
        if self.locked_on:
            self.desired_distance -= offset * self.zoom_sensitivity # How much the mouse wheel moved scaled with sensitivity.
            self.desired_distance = max(0.15, min(self.desired_distance, 2000.0)) # Prevents the distance from moving outside the visual range.
        else:
            forward = glm.normalize(self.current_target - self.position) # Direction to move.
            move_speed = offset * self.zoom_sensitivity # How much the mouse wheel moved scaled with sensitivity.
            self.desired_target += forward * move_speed # Move the target rather than the distance from the target.

    def rotate(self, dx, dy):
        """Rotates the camera around the current target,
           Keeps the target centred in the screen."""
        # How much the mouse moved scaled with sensitivity.
        self.yaw -= dx * self.rotate_sensitivity
        self.pitch -= dy * self.rotate_sensitivity
        # Prevents the camera from flipping over or under the vertical
        max_pitch = glm.radians(89.0)
        self.pitch = max(-max_pitch, min(max_pitch, self.pitch))

    def slide(self, dt, ):
        """Strafes the camera around the simulation,
           the directions are dependent on the cameras' orientation."""
        # Keeps the slide sensitivity similar to the others, but allows for large movements.
        speed = self.slide_sensitivity * dt * 50.0
        world_up = glm.vec3(0.0, 1.0, 0.0) # Y-axis is considered the global up direction.

        # Calculates the Cartesian values for the forward direction relative to the camera.
        forward = glm.vec3(
            math.cos(self.pitch) * math.cos(self.yaw),
            math.sin(self.pitch),
            math.cos(self.pitch) * math.sin(self.yaw)
        )
        right = glm.normalize(glm.cross(world_up, forward)) # Horizontal movement is always perpendicular to the global up and the forward vector
        up = glm.normalize(glm.cross(forward, right)) # Vertical movement is perpendicular to the forward and right directions.

        # Creates a vector as a combination of all directions the user moves.
        movement = glm.vec3(0.0)
        if self.slide_keys["w"]:
            movement += up
        if self.slide_keys["a"]:
            movement -= right
        if self.slide_keys["s"]:
            movement -= up
        if self.slide_keys["d"]:
            movement += right

        # Normalises the movement so it is controlled by the speed.
        if glm.length(movement) > 0.0:
            movement = glm.normalize(movement)
            # Unlocks the camera
            self.locked_on = False
            self.locked_body = None
        self.desired_target += movement * speed

    def update(self, dt):
        """Applies any changes to the desired target and distance so the camera actually moves."""
        # Keeps the camera pointing at a body if set to lock.
        if self.locked_on and self.locked_body:
            self.desired_target = glm.vec3(self.locked_body.position) / DISTANCE_SCALE

        t = min(1.0, dt * self.linear_interp_speed) # The amount the camera can move each loop, creates smooth movement.

        # Moves the camera by the determined amount.
        self.current_target = glm.mix(self.current_target, self.desired_target, t)
        self.current_distance = glm.mix(self.current_distance, self.desired_distance, t)

        # Applies the rotation to the camera.
        pos_x = self.current_target.x + self.current_distance * math.cos(self.pitch) * math.cos(self.yaw)
        pos_y = self.current_target.y + self.current_distance * math.sin(self.pitch)
        pos_z = self.current_target.z + self.current_distance * math.cos(self.pitch) * math.sin(self.yaw)

        self.position = glm.vec3(pos_x, pos_y, pos_z) # Updates the position

    def get_view_matrix(self):
        """
        Uses position and current target to find the cameras direction vector.
        Uses the cross product of the true up vector and the direction to find the cameras right direction vector.
        Uses the cross product of the direction and right vector to find the cameras relative up vector.
        Forms a 4x4 matrix out of these and multiplies by another 4x4 matrix with the last column as the cameras position.
        result is a 4x4 matrix whose last column is the dot products of the cameras position with its own axis,
        multiplying by a position vector gives that position relative to the camera.
        """
        return glm.lookAt(self.position, self.current_target, glm.vec3(0.0, 1.0, 0.0))


    def get_projection_matrix(self):
        """
        Uses the property of similar triangles and the aspect ratio to fit the x and y ordinates into the screen
        Stores the depth value (Z) in an isolated cell, so it can be used to change the sizes later.
        """
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)

    def handle_event(self, event, dt):
        """Sends any mouse or keyboard events directly to the necessary functions"""
        if event.type == py.MOUSEWHEEL:
            self.zoom(event.y)

        # Separates the mouse movement into its two components.
        elif event.type == py.MOUSEMOTION and self.left_mouse_down:
            dx, dy = event.rel
            self.rotate(dx, dy)

        # Enables or disables the camera to be dragged around
        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_mouse_down = True
        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_mouse_down = False

        # Identifies if a key has been pressed or released, holds its state in a dict, smoother than using PyGame's repeating feature.
        elif event.type in (py.KEYDOWN, py.KEYUP):
            down = event.type == py.KEYDOWN
            if event.key == py.K_w:
                self.slide_keys["w"] = down
            elif event.key == py.K_a:
                self.slide_keys["a"] = down
            elif event.key == py.K_s:
                self.slide_keys["s"] = down
            elif event.key == py.K_d:
                self.slide_keys["d"] = down
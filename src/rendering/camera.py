from pyglm import glm
import math
import pygame as py

class Camera:
    def __init__(self,screen_width, screen_height):
        self.current_target = glm.vec3(0.0, 0.0, 0.0)
        self.desired_target = glm.vec3(0.0, 0.0, 0.0)
        self.current_distance = 30
        self.desired_distance = 30
        self.position = glm.vec3(0.0, 0.0, -30.0)
        self.slide_keys = {"w": False, "a": False,"s": False, "d": False}

        self.pitch = glm.radians(0.0)
        self.yaw = glm.radians(90.0)

        self.fov = 45.0
        self.aspect_ratio = screen_width / screen_height
        self.near = 0.1
        self.far = 1000.0

        self.rotate_sensitivity = 0.005
        self.slide_sensitivity = 0.005
        self.zoom_sensitivity = 0.5
        self.linear_interp_speed = 8.0

        self.left_mouse_down = False

    def centre(self):
        self.desired_target = glm.vec3(0.0, 0.0, 0.0)
        self.desired_distance = 30

    def lock_on_body(self, position, radius):
        self.desired_target = glm.vec3(position[0], position[1], position[2])
        self.desired_distance = radius * 6.0

    def zoom(self,offset):
        self.desired_distance -= offset * self.zoom_sensitivity
        self.desired_distance = max(0.1, min(self.desired_distance, 2000.0))

    def rotate(self, dx, dy):
        self.yaw += dx * self.rotate_sensitivity
        self.pitch -= dy * self.rotate_sensitivity
        max_pitch = glm.radians(89.0)
        self.pitch = max(-max_pitch, min(max_pitch, self.pitch))

    def slide(self, dt, ):
        speed = self.current_distance * self.slide_sensitivity * dt * 100.0
        world_up = glm.vec3(0.0, 1.0, 0.0)

        forward = glm.vec3(
            math.cos(self.pitch) * math.cos(self.yaw),
            math.sin(self.pitch),
            math.cos(self.pitch) * math.sin(self.yaw)
        )
        right = glm.normalize(glm.cross(world_up, forward))
        up = glm.normalize(glm.cross(forward, right))

        movement = glm.vec3(0.0)
        if self.slide_keys["w"]:
            movement += up
        if self.slide_keys["a"]:
            movement -= right
        if self.slide_keys["s"]:
            movement -= up
        if self.slide_keys["d"]:
            movement += right

        if glm.length(movement) > 0.0:
            movement = glm.normalize(movement)

        self.desired_target += movement * speed

    def update(self, dt):
        t = min(1.0, dt * self.linear_interp_speed)
        self.current_target = glm.mix(self.current_target, self.desired_target, t)
        self.current_distance = glm.mix(self.current_distance, self.desired_distance, t)

        pos_x = self.current_target.x + self.current_distance * math.cos(self.pitch) * math.cos(self.yaw)
        pos_y = self.current_target.y + self.current_distance * math.sin(self.pitch)
        pos_z = self.current_target.z + self.current_distance * math.cos(self.pitch) * math.sin(self.yaw)

        self.position = glm.vec3(pos_x, pos_y, pos_z)

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
        if event.type == py.MOUSEWHEEL:
            self.zoom(event.y)

        elif event.type == py.MOUSEMOTION and self.left_mouse_down:
            dx, dy = event.rel
            self.rotate(dx, dy)

        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_mouse_down = True

        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_mouse_down = False

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


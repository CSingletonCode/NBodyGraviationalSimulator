#version 330

// The matrices used to move the trail from world space into screen space.
uniform mat4 projection_matrix;
uniform mat4 view_matrix;

in vec3 in_position;

void main() {
    // Positions the trails properly in view space then clip space, sizes are fixed so no model matrix needed.
    gl_Position = projection_matrix * view_matrix * vec4(in_position, 1.0);
}
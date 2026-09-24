#version 330

uniform mat4 projection_matrix;
uniform mat4 view_matrix;

in vec3 in_position;

void main() {
    gl_Position = projection_matrix * view_matrix * vec4(in_position, 1.0);
}
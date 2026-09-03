#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 frag_normal;

void main() {
    // 1. Transform the 3D position into 2D screen space
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);

    // 2. Rotate the normal so it matches the sphere's orientation in the world
    frag_normal = mat3(m_model) * in_normal;
}
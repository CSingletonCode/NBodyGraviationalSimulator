#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 local_position;
out vec3 frag_normal;

void main() {
    local_position = in_position;
    frag_normal = mat3(m_view * m_model) * in_normal;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}

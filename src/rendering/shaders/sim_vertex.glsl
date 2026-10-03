#version 330

// vertex position and its normal recieved from the buffers.
in vec3 in_position;
in vec3 in_normal;

// The matrices used to move the vertex from world space into screen space.
uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

// The values passed on to the fragment shader.
out vec3 local_position;
out vec3 frag_normal;

void main() {
    // base positions are passed straight through
    local_position = in_position;
    // 4th row and coloumn removed from the matrics so translation doesn't change the normals.
    frag_normal = mat3(view_matrix * model_matrix) * in_normal;
    // Transforms the vertex from local space, to world space, to view space and then clip space.
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}

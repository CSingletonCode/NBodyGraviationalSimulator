#version 330

// vertex and texture positions from the buffer
in vec2 base_position;
in vec2 in_uv;

uniform vec2 position;
uniform vec2 size;
uniform vec2 screen_size;

out vec2 uv;

void main()
{
    // send the texture coordinates straight to the fragment shader
    uv = in_uv;

    // normalises the coordinates, scales with the size then moves to the correct position
    vec2 pixel_position = ((base_position + vec2(0.5)) * size) + position;

    // Converts the positions to OpenGL clip positions, between -1 and 1
    vec2 clip_position;
    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;
    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    // sets the final position, with depth as zero so its 2D
    gl_Position = vec4(clip_position, 0.0, 1.0);
}
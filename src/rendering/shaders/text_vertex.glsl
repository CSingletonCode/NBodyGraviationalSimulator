#version 330

in vec2 base_position;
in vec2 in_uv;

uniform vec2 position;
uniform vec2 size;
uniform vec2 screen_size;

out vec2 uv;

void main()
{
    uv = in_uv;

    vec2 pixel_position = ((base_position + vec2(0.5)) * size) + position;

    vec2 clip_position;
    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;

    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    gl_Position = vec4(clip_position, 0.0, 1.0);
}
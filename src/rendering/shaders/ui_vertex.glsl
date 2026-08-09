#version 330

in vec2 base_position; //Default position

uniform vec2 position; //Desired position
uniform vec2 size;
uniform vec2 screen_size;

void main()
{
    // Scale unit rectangle
    vec2 pixel_position = base_position * size;

    // Move from top-left coordinates to centre coordinates
    pixel_position += position + (size*0.5);
    // Convert pixels to OpenGL coordinates
    vec2 clip_position;

    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;

    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    gl_Position = vec4(clip_position, 0.0, 1.0);
}
#version 330

// Default position from the buffers
in vec2 base_position;

uniform vec2 position;
uniform vec2 size;
uniform vec2 screen_size;

void main()
{
    // Expand the shape size to include extra space for a shadow and offset.
    vec2 padding = vec2(1.0, 20.0);
    vec2 expanded_size = size + (padding*2);

    // scales the default shape to the desired size
    vec2 pixel_position = base_position * expanded_size;
    // finds the correct centre for the shape
    pixel_position += position + (size*0.5);

    // normalises the position to the OpenGL -1 to 1 scale
    vec2 clip_position;
    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;
    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    // sets the final position, with depth as zero so its 2D
    gl_Position = vec4(clip_position, 0.0, 1.0);
}
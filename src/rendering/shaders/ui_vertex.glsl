#version 330

in vec2 base_position; //Default position

uniform vec2 position; //Desired position
uniform vec2 size;
uniform vec2 screen_size;

void main()
{
    // adds space for a shadow
    vec2 padding = vec2(1.0, 20.0);

    // expands the size to make room for a shadow
    vec2 expanded_size = size + (padding*2);

    // scales the default shape to the desired size
    vec2 pixel_position = base_position * expanded_size;
    // finds the correct centre for the shape
    pixel_position += position + (size*0.5);

    // changes the pixel position to the openGl normalised coordinate system
    vec2 clip_position;
    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;
    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    gl_Position = vec4(clip_position, 0.0, 1.0);
}
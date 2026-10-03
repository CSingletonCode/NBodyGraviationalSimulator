#version 330

// Texture coordinates recieved from the buffers
in vec2 uv;

// Colour output for the pixel
out vec4 frag_colour;

// The texture containing the elements label.
uniform sampler2D text_texture;

void main()
{
    // Positions the texture at the texture coordinates
    vec4 texture_colour = texture(text_texture, uv);

    frag_colour = texture_colour;
}
#version 330

in vec2 uv;

out vec4 frag_colour;

uniform sampler2D text_texture;

void main()
{
    // It looks at 'text_texture' and gets the colour exactly at the 'uv' coordinates.
    vec4 tex_colour = texture(text_texture, uv);

    frag_colour = tex_colour;
}
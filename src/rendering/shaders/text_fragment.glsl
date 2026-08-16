#version 330

// 1. The data handed to us by the Vertex Shader
in vec2 uv;

// 2. The final color this specific pixel will become
out vec4 frag_colour;

// 3. The Pygame image we uploaded to the GPU (Texture Unit 0)
uniform sampler2D text_texture;

void main()
{
    // "texture()" is a built-in GLSL function.
    // It looks at 'text_texture' and grabs the color exactly at the 'uv' coordinates.
    vec4 tex_colour = texture(text_texture, uv);

    // Output that color directly to the screen!
    frag_colour = tex_colour;
}
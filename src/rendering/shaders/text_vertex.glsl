#version 330

// 1. The raw data coming from your VBO
in vec2 base_position; // The -0.5 to 0.5 shape
in vec2 in_uv;         // The 0.0 to 1.0 texture mapping instructions

// 2. The uniforms passed from your draw_element function
uniform vec2 position;
uniform vec2 size;
uniform vec2 screen_size;

// 3. The data we are passing to the Fragment Shader
out vec2 uv;

void main()
{
    // Pass the UV instructions straight through to the fragment shader
    uv = in_uv;

    // moves the base position to 0 - 1 range, scales to the correct size and moves into position
    vec2 pixel_position = ((base_position + vec2(0.5)) * size) + position;

    // Convert the pixel coordinates into OpenGL "Clip Space" (-1.0 to 1.0)
    vec2 clip_position;
    clip_position.x = ((pixel_position.x / screen_size.x) * 2.0) - 1.0;

    // We invert the Y axis here because OpenGL thinks Y=0 is the BOTTOM of the screen,
    // but Pygame and most UI systems think Y=0 is the TOP of the screen.
    clip_position.y = 1.0 - ((pixel_position.y / screen_size.y) * 2.0);

    // Tell the GPU exactly where this vertex goes
    gl_Position = vec4(clip_position, 0.0, 1.0);
}
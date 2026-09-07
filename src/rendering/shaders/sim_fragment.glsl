#version 330

in vec3 frag_normal;

uniform vec3 light_dir;
uniform vec3 body_colour;

out vec4 frag_colour;

void main() {
    vec3 normal = normalize(frag_normal);
    vec3 l_dir = normalize(light_dir);

    // Dot product for brightness, with 0.1 ambient light so the back isn't pitch black
    float diff = max(dot(normal, l_dir), 0.1);

    vec3 final_colour = body_colour * diff;
    frag_colour = vec4(final_colour, 1.0);
}
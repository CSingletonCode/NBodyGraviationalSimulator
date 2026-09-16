#version 330
in vec3 frag_normal;
in vec3 local_position;

uniform vec3 body_colour;

out vec4 frag_colour;

void main() {
    vec3 normal = normalize(frag_normal);
    vec3 light_direction = vec3(0.0, 0.0, 1.0);

    // Dot product for brightness, with 0.1 ambient light so the back isn't pitch black
    float diff = 1.5*max(dot(normal, light_direction), 0.0);

    vec3 meridian_colour = body_colour * 0.3;
    vec3 equator_colour = body_colour.gbr;

    float ring_thickness = 0.03;
    float meridian_x = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.x));
    float equator = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.y));
    float meridian_z = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.z));

    float on_meridian = max(meridian_x, meridian_z);

    vec3 surface_colour = mix(body_colour, meridian_colour, on_meridian);
    surface_colour = mix(surface_colour, equator_colour, equator);
    vec3 final_colour = clamp(surface_colour * diff, 0.0, 1.0);

    frag_colour = vec4(final_colour, 1.0);
}

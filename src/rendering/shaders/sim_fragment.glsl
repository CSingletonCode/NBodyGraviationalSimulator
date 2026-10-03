#version 330

// Normals in view space and position local to the sphere recieved from the vertex shader
in vec3 frag_normal;
in vec3 local_position;

uniform vec3 body_colour;

out vec4 frag_colour;

void main() {
    // Uses the dot product to find the difference between the normal in view space, and the vector coming straight out of the camera.
    vec3 normal = normalize(frag_normal);
    vec3 light_direction = vec3(0.0, 0.0, 1.0);
    float diff = 1.5 * max(dot(normal, light_direction), 0.0);

    // Uses the bodies colour to get 2 more so the meridian and equator rings always stand out.
    vec3 meridian_colour = body_colour * 0.3;
    vec3 equator_colour = body_colour.gbr;

    // Smooths out the outer edges of the lines, using the 0-1 values from smoothstep
    float ring_thickness = 0.03;
    float meridian_x = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.x));
    float equator = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.y));
    float meridian_z = 1 - smoothstep(ring_thickness*0.5, ring_thickness, abs(local_position.z));

    // selects which ever meridian is closed to the fragment
    float on_meridian = max(meridian_x, meridian_z);

    // merges the body colour with the meridian colour based on how close the fragment is to the meridian.
    vec3 surface_colour = mix(body_colour, meridian_colour, on_meridian);
    // merges that colour with the equator colour so it overrides the connection points with the meridians.
    surface_colour = mix(surface_colour, equator_colour, equator);
    // adds the shadow effect and prevents the values spilling above or below 0 and 1.
    vec3 final_colour = clamp(surface_colour * diff, 0.0, 1.0);

    frag_colour = vec4(final_colour, 1.0);
}

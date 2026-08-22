#version 330

uniform vec4 colour;
uniform vec4 border_colour;
uniform float border_size;
uniform vec2 position;
uniform vec2 size;
uniform float radius;
uniform vec2 screen_size;
uniform bool enable_shadow;
uniform vec2 shadow_offset;
uniform float shadow_blur;

out vec4 frag_colour;

// returns negative if inside shape, positive if outside
float SDF(vec2 point, vec2 halfsize, float radius)
{
    vec2 abs_point = abs(point);

    vec2 q = abs_point - (halfsize - radius);

    float outside_dist = length(max(q, 0.0));
    float inside_dist = min(max(q.x, q.y), 0.0);

    return outside_dist + inside_dist - radius;
}

void main()
{
    // Standardises the fragments cooradinates to (0,0)
    vec2 fragment_position = vec2(gl_FragCoord.x, screen_size.y - gl_FragCoord.y);
    vec2 center = position + (size * 0.5);
    vec2 relative_position = fragment_position - center;

    // Calculates distance from the outer edge of the border
    float outer_dist = SDF(relative_position, size * 0.5, radius);

    // Calculates distance from the inner edge of the border
    vec2 inner_size = size - vec2(border_size * 2.0);
    float inner_radius = max(radius - border_size, 0.0);
    float inner_dist = SDF(relative_position, inner_size * 0.5, inner_radius);

    // Creates a smooth colour blend between the button and its border
    float inner_edge = fwidth(inner_dist); // Determines the rate of change between pixels
    float inner_alpha = 1.0 - smoothstep(-inner_edge, inner_edge, inner_dist); // 0 - 1 value for how much of each colour to use
    vec4 final_colour = mix(border_colour, colour, inner_alpha);

    // Smooths the outer edge with the colour below
    float outer_edge = fwidth(outer_dist);
    float alpha = 1.0 - smoothstep(-outer_edge, outer_edge, outer_dist);

    if (enable_shadow)
    {
        vec4 shadow_colour = vec4(0.0, 0.0, 0.0, 0.5);
        vec2 shadow_position = relative_position - shadow_offset;
        // rounds the shadow like the shape
        float shadow_dist = SDF(shadow_position, size * 0.5, radius);
        // 1.0 so the shadow is
        float shadow_alpha = 1.0 - smoothstep(0.0, shadow_blur, shadow_dist);

        vec2 half_size = size * 0.5;

        // removes the shadow from the sides and above
        float side_fade = 1.0 - smoothstep(half_size.x - 6.0, half_size.x + 4.0, abs(relative_position.x));
        float top_fade = smoothstep(-half_size.y - 4.0, half_size.y * 0.2, relative_position.y);

        // Apply both fades to the shadow
        shadow_alpha *= side_fade * top_fade;

        // Mixes the shadow and the button so a transparent button shows the shadow below.
        vec4 shadow_layer = vec4(shadow_colour.rgb, shadow_colour.a * shadow_alpha);
        vec4 button_colour = vec4(final_colour.rgb, final_colour.a * alpha);
        frag_colour = mix(shadow_layer, button_colour, button_colour.a);
    } else
    {
        frag_colour = vec4(final_colour.rgb, final_colour.a * alpha);
    }
}
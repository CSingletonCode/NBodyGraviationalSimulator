#version 330

// All values from the element to control its shape, colour and position.
uniform vec4 colour;
uniform vec4 border_colour;
uniform float border_size;
uniform vec2 position;
uniform vec2 size;
uniform float radius;
uniform vec2 screen_size;
uniform float ui_scale;
uniform bool enable_shadow;
uniform vec2 shadow_offset;
uniform float shadow_blur;

out vec4 frag_colour;

// Calculates the signed distance from a point to a rounded corner.
// Negatives are inside, positives are outside and 0 is dead on the line.
float SDF(vec2 point, vec2 halfsize, float radius)
{
    // folds all corners into one as the shape is symmetrical.
    vec2 abs_point = abs(point);

    // position relative to the corners
    vec2 q = abs_point - (halfsize - radius);

    // distances from the outer edge on the outside (positive) and inside (negative)
    float outside_dist = length(max(q, 0.0));
    float inside_dist = min(max(q.x, q.y), 0.0);

    // one must be 0 so summing them will handle both
    // - radius to find distance to rounded edge, not corner edge.
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

    // Creates a smooth colour blend between the element and its border
    float inner_edge = fwidth(inner_dist); // Determines how much inner_dist changes between fragments
    float inner_alpha = 1.0 - smoothstep(-inner_edge, inner_edge, inner_dist); // 0 - 1 value for how much of each colour to use
    vec4 final_colour = mix(border_colour, colour, inner_alpha);

    // Smooths the outer edge with the colour below
    float outer_edge = fwidth(outer_dist);
    float alpha = 1.0 - smoothstep(-outer_edge, outer_edge, outer_dist);

    if (enable_shadow)
    {
        vec4 shadow_colour = vec4(0.0, 0.0, 0.0, 0.5);
        // moves the shadow to appear beneath the element.
        vec2 shadow_position = relative_position - shadow_offset;
        // rounds the shadow like the shape
        float shadow_dist = SDF(shadow_position, size * 0.5, radius);

        // Creates an alpha value for blending from the shadow_dist.
        float shadow_alpha = 1.0 - smoothstep(0.0, shadow_blur, shadow_dist);

        vec2 half_size = size * 0.5;

        // removes the shadow from the sides and above
        float side_fade = 1.0 - smoothstep(half_size.x - (6.0 * ui_scale), half_size.x + (4.0 * ui_scale), abs(relative_position.x));
        float top_fade = smoothstep(-half_size.y - (4.0 * ui_scale), half_size.y * (0.2 * ui_scale), relative_position.y);

        // Applies the top and side fades to hide the shadow there.
        shadow_alpha *= side_fade * top_fade;

        // Creates the shadow colour with the calculated opacity.
        vec4 shadow_layer = vec4(shadow_colour.rgb, shadow_colour.a * shadow_alpha);

        // Uses the outer edge alpha to calculate the button colour
        vec4 button_colour = vec4(final_colour.rgb, final_colour.a * alpha);
        frag_colour = mix(shadow_layer, button_colour, button_colour.a);
    } else
    {
        frag_colour = vec4(final_colour.rgb, final_colour.a * alpha);
    }
}
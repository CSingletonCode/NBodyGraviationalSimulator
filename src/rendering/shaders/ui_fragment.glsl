#version 330

uniform vec4 colour;
uniform vec4 border_colour;
uniform float border_size;
uniform vec2 position;
uniform vec2 size;
uniform float radius;
uniform vec2 screen_size;

out vec4 frag_colour;

float SDF(vec2 point, vec2 halfsize, float radius)
{
    vec2 abs_point = abs(point);

    // distance to the edge with the corner removed
    vec2 q = abs_point - (halfsize - radius);

    float outside_dist = length(max(q, 0.0));
    float inside_dist = min(max(q.x, q.y), 0.0);

    return outside_dist + inside_dist - radius;
}

void main()
{
    vec2 fragment_position = vec2(gl_FragCoord.x, screen_size.y - gl_FragCoord.y
);
    vec2 center = position + (size*0.5);

    vec2 relative_posiiton = fragment_position - center;
    float dist = SDF(relative_posiiton, size*0.5, radius);

//    if (dist <= 0.0 && dist >= -1*border_size)
//    {
//        frag_colour = border_colour;
//    }
//    else if (dist < 0.0)
//    {
//        frag_colour = colour;
//    }
//    else
//    {
//        discard;
//    }
//
    float edge = fwidth(dist);
    float alpha = 1.0 - smoothstep(-edge, edge, dist);

    if (alpha <= 0.0)
    {
        discard;
    }

    vec4 final_colour;

    if (dist >= -border_size)
    {
        final_colour = border_colour;
    }
    else
    {
        final_colour = colour;
    }

    frag_colour = vec4(final_colour.rgb, final_colour.a * alpha);
}
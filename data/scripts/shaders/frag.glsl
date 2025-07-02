#version 330 core

uniform sampler2D canvasTex;

in vec2 uvs;
out vec4 f_color;

void main() {
    f_color = vec4(texture(canvasTex, uvs).rgb, 1.0);
}


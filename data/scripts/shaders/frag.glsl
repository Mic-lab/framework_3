#version 330 core

uniform sampler2D canvasTex;
uniform float shakeTimer = -1.0;
uniform float caTimer = -1.0;
in vec2 uvs;
out vec4 f_color;

const float PI = 3.14159265359;
const float caCoef = 0.5;
const float shakeCoef = 0.01;

vec2 rotateVec(vec2 vec, float theta) {
    return vec.x * vec2(cos(theta), sin(theta))
    + vec.y * vec2(sin(theta), -cos(theta));
}

void main() {
    f_color = vec4(texture(canvasTex, uvs).rgb, 1.0);
    float centerDist = distance(uvs, vec2(0.5, 0.5));

    if (shakeTimer >= 0) {
        float shakeIntensity = (1 - shakeTimer)*centerDist * shakeCoef;
        vec2 shakeSampleVec = vec2(0.0, shakeIntensity);
        vec4 caSample1 = texture(canvasTex, uvs + shakeSampleVec);
        vec4 caSample2 = texture(canvasTex, uvs - rotateVec(shakeSampleVec, 2.0*PI/3.0));
        vec4 caSample3 = texture(canvasTex, uvs - rotateVec(shakeSampleVec, 4.0*PI/3.0));
        vec4 sampleMix = mix( mix(caSample1, caSample2, 0.5), caSample3, 0.5 );
        f_color = mix(f_color, sampleMix, 0.5);


        // vec4 caSample1 = vec4(texture(canvasTex, uvs + vec2(shakeIntensity)).rgb, 1.0);
        // vec4 caSample2 = vec4(texture(canvasTex, uvs - vec2(shakeIntensity)).rgb, 1.0);
        // vec4 caSample = mix(caSample1, caSample2, 0.5);
        // f_color = mix(f_color, caSample, (1 - caTimer));
    }

    if (caTimer >= 0) {
        float caIntensity = (1 - caTimer)*centerDist * caCoef;
        vec2 sampleVec = vec2(0.0, caIntensity);
        float caSample1 = texture(canvasTex, uvs + sampleVec).r;
        float caSample2 = texture(canvasTex, uvs - rotateVec(sampleVec, 2.0*PI/3.0)).g;
        float caSample3 = texture(canvasTex, uvs - rotateVec(sampleVec, 4.0*PI/3.0)).b;
        f_color.r = caSample1;
        f_color.g = caSample2;
        f_color.b = caSample3;
    }
    
}


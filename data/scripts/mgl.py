from array import array
import moderngl
from .utils import read_file

ctx = moderngl.create_context()

quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,   # topleft
    1.0, 1.0, 1.0, 0.0,    # topright
    -1.0, -1.0, 0.0, 1.0,  # bottomleft
    1.0, -1.0, 1.0, 1.0,   # bottomright
]))

vert_shader = read_file('data/scripts/shaders/vert.glsl')
frag_shader = read_file('data/scripts/shaders/frag.glsl')

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf2tex(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

def update_tex(tex, surf):
    tex.write(surf.get_view('1'))
    return tex


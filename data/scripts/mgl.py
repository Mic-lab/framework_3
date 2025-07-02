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

shader_surfs = []

def surf2tex(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

def update_tex(tex, surf):
    tex.write(surf.get_view('1'))
    return tex

shader_surfs_ids = {}
used_textures = []
def transfer_shader_surfs(shader_surfs: dict):
    for surf_key, surf in shader_surfs.items():
        if surf_key not in shader_surfs_ids:
            surf_id = len(shader_surfs_ids)
            shader_surfs_ids[surf_key] = surf_id
        else:
            surf_id = shader_surfs_ids[surf_key]

        tex = surf2tex(surf)
        tex.use(surf_id)
        program[surf_key] = surf_id
        used_textures.append(tex)

def release_textures():
    for tex in used_textures:
        tex.release()

    used_textures.clear()


    # frame_tex = mgl.surf2tex(surf)


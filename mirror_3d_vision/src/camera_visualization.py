
import numpy as np

import moderngl
import os
import moderngl
import numpy as np
from pyrr import Matrix44

import moderngl_window as mglw


def makeProgram(ctx):
    return ctx.program(vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_position;
                in vec3 in_normal;
                in vec2 in_texcoord_0;

                out vec3 v_vert;
                out vec3 v_norm;
                out vec2 v_text;

                void main() {
                    gl_Position = Mvp * vec4(in_position, 1.0);
                    v_vert = in_position;
                    v_norm = in_normal;
                    v_text = in_texcoord_0;
                }
            ''',
            fragment_shader='''
                #version 330

                uniform vec3 Light;
                uniform sampler2D Texture;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
                    f_color = vec4(texture(Texture, v_text).rgb * lum, 1.0);
                }
            ''',
        )


# prepare geometry
def star(inner=0.45, outer=1.0, n=5):
    R = np.array([inner, outer] * n)
    T = np.linspace(-0.5 * np.pi, 1.5 * np.pi, 2 * n, endpoint=False)
    P = np.zeros((2 * n, 3))
    P[:, 0] = R * np.cos(T)
    P[:, 1] = R * np.sin(T)

    return np.vstack([P, P[0]])


# prepare geometry
def camera():
    n = 10
    P = np.zeros((n, 3))
    P[:, 0] = [-1,-1, 1, 1,-1,-1,-1, 1, 1,-1,]
    P[:, 1] = [-1, 1, 1,-1,-1,-1, 1, 1,-1,-1,]
    P[:, 2] = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,]

    return np.vstack([P, P[0]])

def rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])


def build_buffers(lines):
    """Prepare the buffers for multi-polyline rendering. Closed polyline must have their
    last point identical to their first point."""

    lines = [np.array(line, dtype="f4") for line in lines]

    indices = []
    reset_index = [-1]
    start_index = 0
    for line in lines:
        if np.all(line[0] == line[-1]):  # closed path
            idx = np.arange(len(line) + 3) - 1
            idx[0], idx[-2], idx[-1] = len(line) - 1, 0, 1
        else:
            idx = np.arange(len(line) + 2) - 1
            idx[0], idx[-1] = 0, len(line) - 1

        indices.append(idx + start_index)
        start_index += len(line)
        indices.append(reset_index)

    return np.vstack(lines).astype("f4"), np.concatenate(indices).astype("i4")

class CrateExample(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    resource_dir = os.path.normpath(os.path.join(__file__, '../'))

    title = "Crate"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        prog = makeProgram(self.ctx)

        self.mvp = prog['Mvp']
        self.light = prog['Light']

        self.scene = self.load_scene('crate.obj')
        self.vao = self.scene.root_nodes[0].mesh.vao.instance(prog)
        self.texture = self.load_texture_2d('crate.png')

        lines = [[0,0,0,0], [10,2,2,0]]
        line_indexes = [0, 1, 0, 1]

        vbo = self.ctx.buffer(np.vstack(lines).astype("f4"))
        ibo = self.ctx.buffer(np.array(line_indexes).astype("i4"))
        self.line_prog = self.load_program("rich_lines.glsl")
        self.line_prog["linewidth"].value = 15
        self.line_prog["antialias"].value = 1.5
        self.line_prog["miter_limit"].value = -1
        self.line_prog["color"].value = 0, 0, 1, 1
        self.linevao = self.ctx.simple_vertex_array(self.line_prog, vbo, "position",
                                                index_buffer=ibo)

        lines = [
            star(n=5) * 3 + (0, 0, 0),
            star(n=8) * 1 + (0,0,1),
            camera(),
        ]

        vertex, index = build_buffers(lines)

        vbo = self.ctx.buffer(vertex)
        ibo = self.ctx.buffer(index)
        self.linevao = self.ctx.simple_vertex_array(self.line_prog, vbo, "position",
                                                index_buffer=ibo)

        self.line_prog["linewidth"].write(np.array(0.1, dtype="f4"))

        self.line_prog["projection"].write(
            Matrix44.orthogonal_projection(0, 1600, 800, 0, 0.5, -0.5, dtype="f4")
        )


    def render(self, time, frame_time):
        angle = time
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        camera_pos = (np.cos(angle) * 3.0, np.sin(angle) * 3.0, 2.0)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)
        lookat = Matrix44.look_at(
            camera_pos,
            (0.0, 0.0, 0.5),
            (0.0, 0.0, 1.0),
        )

        self.mvp.write((proj * lookat).astype('f4'))
        self.light.value = camera_pos
        self.texture.use()
        self.vao.render()

        move = Matrix44.from_translation((0.0,0.0,0.5))

        self.mvp.write(( proj * lookat  * move).astype('f4'))
        self.light.value = camera_pos
        self.texture.use()
        self.vao.render()

        self.line_prog["projection"].write(
            ( proj * lookat ).astype('f4')
        )

        projec = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0, dtype="f4")*lookat

        orthag = Matrix44.orthogonal_projection(-1600, 1600, 800, -800, 0.5, -0.5, dtype="f4")
        the_mat = projec
        self.line_prog["projection"].write(
            the_mat.astype("f4")
        )

        self.linevao.render(moderngl.LINE_STRIP_ADJACENCY)



if __name__ == '__main__':
    mglw.run_window_config(CrateExample)


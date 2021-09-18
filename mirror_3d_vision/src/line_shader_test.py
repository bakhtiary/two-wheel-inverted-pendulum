import os
import moderngl
import numpy as np
from pyrr import Matrix44

import moderngl_window as mglw


def star(inner=0.45, outer=1.0, n=5):
    R = np.array([inner, outer] * n)
    T = np.linspace(-0.5 * np.pi, 1.5 * np.pi, 2 * n, endpoint=False)
    P = np.zeros((2 * n, 4))
    P[:, 0] = R * np.cos(T)
    P[:, 1] = R * np.sin(T)

    return P

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

        lines = [
            (star(n=5) + (0, 0, 0, -1)),
        ]

        vertex, index = build_buffers(lines)
        print(vertex)
        index = list([0,1,2,3,1,2,3,4,2,3,4,5,3,4,5,6,4,5,6,7,5,6,7,8,6,7,8,9,7,8,9,0,8,9,0,1,9,0,1,2])

        self.line_prog = self.load_program("crappy_lines.glsl")
        vbo = self.ctx.buffer(vertex)
        ibo = self.ctx.buffer(np.array(index).astype("i4"))
        self.linevao = self.ctx.simple_vertex_array(self.line_prog, vbo, "Vertex",index_buffer=ibo)

        self.line_prog["Thickness"].write(np.array([2.0],dtype="f4"))
        self.line_prog["Viewport"].write(np.array([1280, 720],dtype="f4"))
        self.line_prog["MiterLimit"].write(np.array(0.1, dtype="f4"))


    def render(self, time, frame_time):
        angle = time
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        camera_pos = (np.cos(angle) * 30.0, np.sin(angle) * 30.0, 20.0)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 200.0)
        lookat = Matrix44.look_at(
            camera_pos,
            (0.0, 0.0, 0.5),
            (0.0, 0.0, 1.0),
        )

        self.line_prog["ModelViewProjectionMatrix"].write(
            (proj*lookat).astype("f4")
        )

        self.linevao.render(moderngl.LINES_ADJACENCY)



if __name__ == '__main__':
    mglw.run_window_config(CrateExample)

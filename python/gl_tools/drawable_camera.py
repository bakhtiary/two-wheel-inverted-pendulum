import os
import moderngl
import numpy as np
from pyrr import Matrix44

import moderngl_window as mglw

def make_flat_square():
    P = np.zeros((5, 3))
    P[:, 0] = [-1, -1, 1, 1, -1,]
    P[:, 1] = [-1, 1, 1, -1, -1,]
    P[:, 2] = [0, 0, 0, 0, 0,]
    return P

class Camera_wireframe:

    def __init__(self, windowConfig, texture_name):
        ctx = windowConfig.ctx
        self.prog = windowConfig.load_program("src/gl_tools/crappy_lines.glsl")

        bottom = make_flat_square()
        top = (make_flat_square()*1.5) + [0,0,2]

        self.vertex = np.vstack([bottom,top]).astype("f4")
        number_of_vertexes = len(self.vertex)
        index = get_indexes_of_line_through_all_vertexes(number_of_vertexes)
        vbo = ctx.buffer(self.vertex)
        ibo = ctx.buffer(np.array(index).astype("i4"))
        self.linevao = ctx.simple_vertex_array(self.prog, vbo, "Vertex", index_buffer=ibo)
        self.prog["Thickness"].write(np.array([2.0], dtype="f4"))
        self.prog["Viewport"].write(np.array([1280, 720], dtype="f4"))
        self.prog["MiterLimit"].write(np.array(0.1, dtype="f4"))

        self.mesh_prog = windowConfig.load_program("src/gl_tools/textured_mesh.glsl")
        scene = windowConfig.load_scene('src/gl_tools/plane_mesh.obj')
        self.vao = scene.root_nodes[0].mesh.vao.instance(self.mesh_prog)
        self.texture = windowConfig.load_texture_2d(texture_name)
        self.mvp = self.mesh_prog['Mvp']
        self.light = self.mesh_prog['Light']



    def render(self, projection_matrix):
        self.prog["ModelViewProjectionMatrix"].write(projection_matrix)
        self.linevao.render(moderngl.LINES_ADJACENCY)

        self.mvp.write((projection_matrix).astype("f4"))
        self.light.value = (0.0,0.0,1.0)
        self.texture.use()
        self.vao.render()


def get_indexes_of_line_through_all_vertexes(number_of_vertexes):
    return [j % number_of_vertexes for i in range(number_of_vertexes) for j in range(i, i + 4)]


class CrateExample(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    resource_dir = os.getcwd()

    title = "Crate"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.camera = Camera_wireframe(self,(os.getcwd()+"/calib_fotos/2.jpg"))

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

        camera_matrix = (proj * lookat).astype("f4")

        self.camera.render(camera_matrix)


if __name__ == '__main__':
    mglw.run_window_config(CrateExample)

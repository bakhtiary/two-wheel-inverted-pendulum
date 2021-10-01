
import os
import moderngl
import numpy as np
from pyrr import Matrix44

import moderngl_window as mglw

class Crate_mesh():

    def __init__(self, windowConfig):
        self.prog = windowConfig.load_program("src/gl_tools/textured_mesh.glsl")
        scene = windowConfig.load_scene('src/gl_tools/crate.obj')
        self.vao = scene.root_nodes[0].mesh.vao.instance(self.prog)
        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']
        self.texture = windowConfig.load_texture_2d('src/gl_tools/crate.png')


    def render(self, projection_matrix):
        self.mvp.write(projection_matrix)
        self.light.value = (1.0,1.0,1.0)
        self.texture.use()
        self.vao.render()


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

        self.crate = Crate_mesh(self)

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

        self.crate.render((proj*lookat).astype("f4"))




if __name__ == '__main__':
    mglw.run_window_config(CrateExample)


import math
import multiprocessing
import os
import sys

import moderngl
import numpy as np
from moderngl_window.context.base import KeyModifiers
from pyrr import Matrix44

import moderngl_window as mglw

from gl_tools.drawable_camera import Camera_wireframe
from gl_tools.drawable_crate import Crate_mesh

def rodrigues_vec_to_rotation_mat(rodrigues_vec):
    theta = np.linalg.norm(rodrigues_vec)
    if theta < sys.float_info.epsilon:
        rotation_mat = np.eye(3, dtype=float)
    else:
        r = rodrigues_vec / theta
        I = np.eye(3, dtype=float)
        r_rT = np.array([
            [r[0]*r[0], r[0]*r[1], r[0]*r[2]],
            [r[1]*r[0], r[1]*r[1], r[1]*r[2]],
            [r[2]*r[0], r[2]*r[1], r[2]*r[2]]
        ])
        r_cross = np.array([
            [0, -r[2], r[1]],
            [r[2], 0, -r[0]],
            [-r[1], r[0], 0]
        ])
        rotation_mat = math.cos(theta) * I + (1 - math.cos(theta)) * r_rT + math.sin(theta) * r_cross
    return rotation_mat

class Composition:

    def __init__(self):
        self.things_to_render = []

    def camera_location(self,camera_pos,aspect_ratio):
        proj = Matrix44.perspective_projection(45.0, aspect_ratio, 0.1, 200.0)
        lookat = Matrix44.look_at(
            camera_pos,
            (0.0, 0.0, 20),
            (0.0, 0.0, 1.0),
        )

        self.camera_matrix = (proj * lookat).astype("f4")

    def add(self, drawable, position, rotation):
        self.things_to_render.append([drawable, position, rotation])
        return len(self.things_to_render) - 1

    def update_pos_rot(self, index, position, rotation):
        self.things_to_render[index][1] = position
        self.things_to_render[index][2] = rotation

    def render(self):
        for drawable,pos,rot in self.things_to_render:
            pos_mat = Matrix44.from_translation(pos)
            rot_mat = rodrigues_vec_to_rotation_mat(np.array(rot))
            drawable.render((self.camera_matrix*pos_mat*rot_mat).astype("f4"))


def runBoardLocationViewer(location_queue: multiprocessing.Queue):
    class CalibrationViewer(mglw.WindowConfig):

        gl_version = (3, 3)
        title = "ModernGL Example"
        window_size = (1280, 720)
        aspect_ratio = 16 / 9
        resizable = True
        resource_dir = os.getcwd()
        title = "Crate"

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.composition = Composition()
            self.crate = Crate_mesh(self)
            self.dist = 40
            self.angle = 0

            self.board_id = self.composition.add(Crate_mesh(self), [0, 0, 0], [])

        def render(self, time, frame_time):
            self.ctx.clear(0.0, 0.0, 0.0)
            self.ctx.enable(moderngl.DEPTH_TEST)
            angle = self.angle

            if not location_queue.empty():
                board_rot, board_loc = location_queue.get()
                print(f"{board_rot}, {board_loc }")
                self.composition.update_pos_rot(self.board_id, board_loc.flatten(), board_rot.flatten())

            self.composition.camera_location(
                camera_pos=(np.cos(angle) * self.dist, np.sin(angle) * self.dist, self.dist*0.70 + 20),
                aspect_ratio=self.aspect_ratio
            )

            self.composition.render()

        def key_event(self, key, action, modifiers: KeyModifiers):

            print (key, action)
            if action == self.wnd.keys.ACTION_PRESS:
                if key == ord('w'):
                    self.dist *= 0.9
                if key == ord('s'):
                    self.dist *= 1.1
                if key == ord('a'):
                    self.angle += 0.01
                if key == ord('d'):
                    self.angle -= 0.01

    mglw.run_window_config(CalibrationViewer)

if __name__ == '__main__':
    exit(0)
    from numpy import array
    q = multiprocessing.Queue()

    runBoardLocationViewer(q)

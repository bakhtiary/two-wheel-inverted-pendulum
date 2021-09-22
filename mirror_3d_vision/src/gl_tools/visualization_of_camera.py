import math
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
            (0.0, 0.0, 0.5),
            (0.0, 0.0, 1.0),
        )

        self.camera_matrix = (proj * lookat).astype("f4")

    def add(self, drawable, position, rotation):
        self.things_to_render.append((drawable, position, rotation))

    def render(self):
        for drawable,pos,rot in self.things_to_render:
            pos_mat = Matrix44.from_translation(pos)
            rot_mat = rodrigues_vec_to_rotation_mat(np.array(rot))
            drawable.render((self.camera_matrix*rot_mat*pos_mat).astype("f4"))



def runCalibrationViewer(camera_pos_list, camera_rot_list, image_name_list):
    class CalibrationViewer(mglw.WindowConfig):
        camera_pos_list
        camera_rot_list
        image_name_list
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
            self.composition.add(Crate_mesh(self), [0,0,0], [])
            self.dist = 40
            for cam_loc, cam_rot, image_name in zip(camera_pos_list, camera_rot_list, image_name_list):
                self.composition.add(Camera_wireframe(self, image_name), cam_loc.flatten(), cam_rot.flatten())
            self.angle = 0

        def render(self, time, frame_time):
            self.ctx.clear(0.0, 0.0, 0.0)
            self.ctx.enable(moderngl.DEPTH_TEST)

            self.composition.camera_location(
                camera_pos = (np.cos(self.angle) * self.dist, np.sin(self.angle) * self.dist, self.dist*0.70),
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
    from numpy import array
    camera_loc_list = [
        array([[1.77897703],
               [0.26029351],
               [1.11745587]]),
        array([[-3.27518137], [-2.26986732], [13.21556809]]),
        array([[-3.20727923], [-3.18571279], [ 9.07769199]]),
        array( [[-1.81526951], [-2.61015036], [19.02358253]]),
    ]
    camera_rot_list = [
        array([[0.29515454],
               [-0.39019976],
               [-3.38643238]]),

        array([[-0.62631573], [-0.04096639], [ 0.10316385]]),
        array([[-0.08141961], [-0.04832145], [ 0.06116317]]),
        array([[-0.00091781], [ 0.09203101], [ 0.09375997]]),
    ]
    camera_image_list = [

        "charucho_fotos/1.jpg",
        "./calib_fotos/10.jpg",
        "./calib_fotos/11.jpg",
        "./calib_fotos/12.jpg",
    ]

    runCalibrationViewer(camera_loc_list, camera_rot_list, camera_image_list)

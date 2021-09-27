import dataclasses

import cv2

from Capability import Capability



class VideoSource:

    def get_source(self):
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        @dataclasses.dataclass
        class CapSpec:
            def __init__(self, name, val, inc=None, key=None):
                self.name = name
                self.val = val
                self.inc = inc
                self.key = key

        all_caps = [
            CapSpec("CAP_PROP_FRAME_WIDTH", 1920),
            CapSpec("CAP_PROP_FRAME_HEIGHT", 1080),
            CapSpec("CAP_PROP_EXPOSURE", -11.0, 1, 'e'),
            CapSpec("CAP_PROP_AUTOFOCUS", 0.0),
            CapSpec("CAP_PROP_FOCUS", 0, 1, 'f'),
            CapSpec("CAP_PROP_WHITE_BALANCE_BLUE_U", 0.0,100,'B'),
            CapSpec("CAP_PROP_BACKLIGHT", 1),
            CapSpec("CAP_PROP_CONTRAST", 0, 8, 'c'),
            CapSpec("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpec("CAP_PROP_SHARPNESS", 128, 8, 's'),
            CapSpec("CAP_PROP_GAIN", 255),
            CapSpec("CAP_PROP_PAN", 10, 1, 'p'),
        ]

        capability_map = {}
        for c in all_caps:
            capability_id = cv2.__dict__[c.name]
            vid.set(capability_id, c.val)
            if c.key is not None:
                capability_map[c.key] = Capability(capability_id, c.val, c.inc, c.name)

        return vid, capability_map


class CameraEye:
    def __init__(self, video_source: VideoSource):
        self.video_source: VideoSource = video_source
        self.capability_map = None
        self.calibration_matrix = None
        self.dist_coef = None


    def calibrate(self, calibration_matrix):
        self.calibration_matrix = calibration_matrix

    @classmethod
    def c29_webcam_eye(cls):
        return CameraEye(VideoSource())

    def open_eyes(self):
        self.vid, self.capability_map = self.video_source.get_source()

    def close_eyes(self):
        self.vid.release()
        self.vid = None


    def set_calibration_parameters(self, calibration_matrix, dist_coef):
        self.calibration_matrix = calibration_matrix
        self.dist_coef = dist_coef

    def get_next_image(self):
        return self.vid.read()


    def send_event(self, the_char):
        capability = self.capability_map[the_char.lower()]
        direction = -1 if the_char.islower() else 1
        capability.cur_value += capability.increment * direction
        self.vid.set(capability.id, capability.cur_value)
        print(f"changed value of {capability.print_name} to {capability.cur_value}")
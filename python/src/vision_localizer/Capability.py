import dataclasses
from dataclasses import dataclass

import cv2


@dataclass
class Capability:
    id: int
    increment: int
    print_name: str


@dataclass
class CapSpec:
    name: str
    initial_val: float
    increment: int = None
    assigned_key: str = None


class VideoSource:

    def get_vid(self):
        raise NotImplementedError()

    def get_cap_specs(self):
        raise NotImplementedError()

    def get_source(self):
        vid = self.get_vid()

        capability_map = {}

        all_caps = self.get_cap_specs()

        for c in all_caps:
            capability_id = cv2.__dict__[c.name]
            vid.set(capability_id, c.initial_val)
            if c.assigned_key is not None:
                capability_map[c.assigned_key] = Capability(capability_id, c.increment, c.name)

        return vid, capability_map


class C299_linux_Spec_Factory(VideoSource):
    def get_vid(self):
        vid = cv2.VideoCapture("/dev/video0")
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpec("CAP_PROP_FRAME_WIDTH", 1920),
            CapSpec("CAP_PROP_FRAME_HEIGHT", 1080),
            CapSpec("CAP_PROP_AUTO_EXPOSURE", 0, 1),
            CapSpec("CAP_PROP_EXPOSURE", -11.0, 5, 'e'),
            CapSpec("CAP_PROP_AUTOFOCUS", 0.0),
            CapSpec("CAP_PROP_FOCUS", 0, 5, 'f'),
            CapSpec("CAP_PROP_WHITE_BALANCE_BLUE_U", 0.0, 100, 'b'),
            CapSpec("CAP_PROP_BACKLIGHT", 1),
            CapSpec("CAP_PROP_CONTRAST", 0, 8, 'c'),
            CapSpec("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpec("CAP_PROP_SHARPNESS", 128, 8, 's'),
            CapSpec("CAP_PROP_GAIN", 255),
            CapSpec("CAP_PROP_PAN", 10, 1, 'p'),
        ]


class C299_win_Spec_Factory(VideoSource):
    def get_vid(self):
        vid = cv2.VideoCapture(0)
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpec("CAP_PROP_FRAME_WIDTH", 1920),
            CapSpec("CAP_PROP_FRAME_HEIGHT", 1080),
            CapSpec("CAP_PROP_AUTO_EXPOSURE", 0, 1),
            CapSpec("CAP_PROP_EXPOSURE", -11.0, 5, 'e'),
            CapSpec("CAP_PROP_AUTOFOCUS", 0.0),
            CapSpec("CAP_PROP_FOCUS", 0, 5, 'f'),
            CapSpec("CAP_PROP_WHITE_BALANCE_BLUE_U", 0.0, 100, 'b'),
            CapSpec("CAP_PROP_BACKLIGHT", 1),
            CapSpec("CAP_PROP_CONTRAST", 0, 8, 'c'),
            CapSpec("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpec("CAP_PROP_SHARPNESS", 128, 8, 's'),
            CapSpec("CAP_PROP_GAIN", 255),
            CapSpec("CAP_PROP_PAN", 10, 1, 'p'),
        ]


class Cheap_Cam_Linux_Spec_Factory():
    def get_vid(self):
        vid = cv2.VideoCapture("/dev/video1")
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpec("CAP_PROP_CONTRAST", 128, 8, 'c'),
            CapSpec("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpec("CAP_PROP_SATURATION", 128, 8, 's'),
            CapSpec("CAP_PROP_SHARPNESS", 128, 8, 's'),
            # CapSpec("CAP_PROP_HUE", 0, 1, 'h'),
            # CapSpec("CAP_PROP_GAMMA", 4, 1, 'g'),
            CapSpec("CAP_PROP_BACKLIGHT", 4, 1, 'l'),
        ]

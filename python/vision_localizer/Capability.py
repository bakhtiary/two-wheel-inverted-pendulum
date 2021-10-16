from dataclasses import dataclass

import cv2

@dataclass
class CapSpecs:
    name: str
    initial_val: float
    increment: int = None
    assigned_key: str = None
    min_val: int = None
    max_val: int = None
    capability_id = None

    def __post_init__(self):
        self.capability_id = cv2.__dict__[self.name]
        self.initial_val = self.constrain(self.initial_val)

    def constrain(self, m):
        if self.min_val is not None and m < self.min_val:
            print(f"{m} is lower than minval for {self.name} so resetting it")
            m = self.min_val
        elif self.max_val is not None and m > self.max_val:
            m = self.max_val
        return m


class VideoSource:

    def get_vid(self):
        raise NotImplementedError()

    def get_cap_specs(self) -> list[CapSpecs]:
        raise NotImplementedError()

    def get_source(self):
        vid = self.get_vid()
        capability_map = {}
        all_caps = self.get_cap_specs()
        for c in all_caps:

            vid.set(c.capability_id, c.initial_val)
            if c.assigned_key is not None:
                capability_map[c.assigned_key] = c

        return vid, capability_map


class C299_linux_Spec_Factory(VideoSource):
    def get_vid(self):
        vid = cv2.VideoCapture("/dev/video0")
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpecs("CAP_PROP_FRAME_WIDTH", 800),
            CapSpecs("CAP_PROP_FRAME_HEIGHT", 600),
            CapSpecs("CAP_PROP_AUTO_EXPOSURE", 0.0, 1, ';'),
            CapSpecs("CAP_PROP_EXPOSURE", 0, 5, 'e', 0),
            CapSpecs("CAP_PROP_AUTOFOCUS", 0.0),
            CapSpecs("CAP_PROP_FOCUS", 0, 5, 'f', 0),
            CapSpecs("CAP_PROP_WHITE_BALANCE_BLUE_U", 0.0, 100, 'b'),
            CapSpecs("CAP_PROP_BACKLIGHT", 1),
            CapSpecs("CAP_PROP_CONTRAST", 0, 8, 'c', 0),
            CapSpecs("CAP_PROP_BRIGHTNESS", 128, 8, 'b', 0),
            CapSpecs("CAP_PROP_SHARPNESS", 128, 8, 's', 0),
            CapSpecs("CAP_PROP_GAIN", 128, 1, 'g', 0, 255),
            CapSpecs("CAP_PROP_PAN", 36000, 1000, 'p'),
        ]


class C299_win_Spec_Factory(VideoSource):
    def get_vid(self):
        vid = cv2.VideoCapture(0)
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpecs("CAP_PROP_FRAME_WIDTH", 320),
            CapSpecs("CAP_PROP_FRAME_HEIGHT", 240),
            CapSpecs("CAP_PROP_AUTO_EXPOSURE", 0, 1),
            CapSpecs("CAP_PROP_EXPOSURE", -11.0, 5, 'e'),
            CapSpecs("CAP_PROP_AUTOFOCUS", 0.0),
            CapSpecs("CAP_PROP_FOCUS", 0, 5, 'f'),
            CapSpecs("CAP_PROP_WHITE_BALANCE_BLUE_U", 0.0, 100, 'b'),
            CapSpecs("CAP_PROP_BACKLIGHT", 1),
            CapSpecs("CAP_PROP_CONTRAST", 0, 8, 'c'),
            CapSpecs("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpecs("CAP_PROP_SHARPNESS", 128, 8, 's'),
            CapSpecs("CAP_PROP_GAIN", 255),
            CapSpecs("CAP_PROP_PAN", 20, 1000, 'p'),
        ]


class Cheap_Cam_Linux_Spec_Factory():
    def get_vid(self):
        vid = cv2.VideoCapture("/dev/video1")
        if not vid.isOpened():
            raise Exception("Error could not connect to camera")

        return vid

    def get_cap_specs(self):
        return [
            CapSpecs("CAP_PROP_CONTRAST", 128, 8, 'c'),
            CapSpecs("CAP_PROP_BRIGHTNESS", 128, 8, 'b'),
            CapSpecs("CAP_PROP_SATURATION", 128, 8, 's'),
            CapSpecs("CAP_PROP_SHARPNESS", 128, 8, 's'),
            CapSpecs("CAP_PROP_HUE", 0, 1, 'h'),
            CapSpecs("CAP_PROP_GAMMA", 4, 1, 'g'),
            CapSpecs("CAP_PROP_BACKLIGHT", 4, 1, 'l'),
        ]

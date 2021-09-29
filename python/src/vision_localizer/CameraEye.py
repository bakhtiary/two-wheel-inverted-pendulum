from Capability import C299_linux_Spec_Factory, C299_win_Spec_Factory, CapSpecs
from vision_localizer.Capability import VideoSource


class CameraEye:
    def __init__(self, video_source: VideoSource):
        self.video_source: VideoSource = video_source
        self.capability_map: dict[str, CapSpecs] = None
        self.calibration_matrix = None
        self.dist_coef = None
        self.direction = +1

    def calibrate(self, calibration_matrix):
        self.calibration_matrix = calibration_matrix

    @classmethod
    def c29_webcam_linux_eye(cls):
        return CameraEye(C299_linux_Spec_Factory())

    @classmethod
    def c29_webcam_win_eye(cls):
        return CameraEye(C299_win_Spec_Factory())

    def open_eyes(self):
        self.vid, self.capability_map = self.video_source.get_source()
        self.capability_map['='] = None
        self.capability_map['-'] = None
        self.capability_map['+'] = None
        self.capability_map['_'] = None

    def close_eyes(self):
        self.vid.release()
        self.vid = None

    def set_calibration_parameters(self, calibration_matrix, dist_coef):
        self.calibration_matrix = calibration_matrix
        self.dist_coef = dist_coef

    def get_next_image(self):
        return self.vid.read()

    def send_event(self, the_char):
        if the_char == '=':
            self.direction = +1
        elif the_char == '+':
                self.direction = +10
        elif the_char == '-':
            self.direction = -1
        elif the_char == '_':
            self.direction = -10
        else:
            capability = self.capability_map[the_char.lower()]
            cur_value = self.vid.get(capability.capability_id)
            cur_value += capability.increment * self.direction
            cur_value = capability.constrain(cur_value)
            self.vid.set(capability.capability_id, cur_value)
            print(f"changed value of {capability.name} to {cur_value}")

    def print_spec_values(self):
        for cap_spec in self.video_source.get_cap_specs():
            print(f"{cap_spec.name}: {self.vid.get(cap_spec.capability_id)}")

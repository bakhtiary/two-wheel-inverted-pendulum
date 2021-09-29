import dataclasses
from dataclasses import dataclass


@dataclass
class Capability:
    id: int
    increment: int
    print_name: str


@dataclasses.dataclass
class CapSpec:
    name: str
    initial_val: float
    increment: int = None
    assigned_key: str = None


class C299_linux_Spec_Factory:
    def get_src
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

class C299_win_Spec_Factory:
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
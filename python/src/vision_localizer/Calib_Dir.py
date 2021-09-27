import os
import traceback
from glob import glob


class Calib_Dir:
    def __init__(self, directory):
        self.directory = directory
        self.current_image_number = 0
        os.makedirs(self.directory, exist_ok=True)
        if os.path.exists(self.image_number_file()):
            try:
                with open(self.image_number_file()) as number_file:
                    self.current_image_number = int(number_file.readline())
            except:
                traceback.print_exc()
                print("Warning: failed to read image_number, setting it to zero. Images will be over written")
                self.current_image_number = 0

    def image_number_file(self):
        return os.path.join(self.directory, "current_image_number")

    def calibration_matrix_filename(self):
        return os.path.join(self.directory, "calibration_matrix")

    def get_next_image_name(self):
        with open(self.image_number_file(),"w") as number_file:
            number_file.writelines(str(self.current_image_number))
        self.current_image_number += 1
        return os.path.join(self.directory, f"{self.current_image_number}.jpeg")

    def stored_image_files(self):
        return glob(f"{self.directory}/*.jpeg")

    def calibration_distCoefs_filename(self):
        return os.path.join(self.directory, "calibration_distcoefs")


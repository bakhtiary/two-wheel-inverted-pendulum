import struct

import onnx

import numpy as np


def get_cpp_definition(onnx_model):
    raw_def = ""
    for i, initializer in enumerate(onnx_model.graph.initializer):
        format_spec = f"{len(initializer.raw_data) // 4}f"
        with np.printoptions(floatmode='unique'):
            float_data = np.array(struct.unpack_from(format_spec, initializer.raw_data))

        raw_def += f"""

float {initializer.name.replace('.', '_')}[] {{ 
        {np.array2string(float_data, separator=',', floatmode='unique', threshold=10000000, )};
}};
        """
    return raw_def




with open("weight_definitions.h", "w") as header_file:
    onnx_model = onnx.load("actor_model.onnx")  # load onnx model
    print(get_cpp_definition(onnx_model))


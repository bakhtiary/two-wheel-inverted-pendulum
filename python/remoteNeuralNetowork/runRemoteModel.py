import onnx
import numpy as np
import struct
import functools
from functools import reduce

from remoteNeuralNetowork.get_id_param_pair import get_id_param_pair_iterator

onnx_model = onnx.load("actor_model.onnx")  # load onnx model


def make_param_definition_header(onnx_model, header_file):
    params_def = "#define NUM(a) (sizeof(a) / sizeof(*a))\n"
    for i, initializer in get_id_param_pair_iterator(onnx_model):
        format_spec = f"{len(initializer.raw_data) // 4}f"
        float_data = np.array(struct.unpack_from(format_spec, initializer.raw_data))
        value_names = initializer.name.replace('.', '_')
        raw_def = f""" float {value_names}[]{{ {
        functools.reduce(lambda a, b: a + ", " + b, map(lambda x: f"{x:.30f}", float_data))
        } }};
        """
        header_file.write(raw_def)
        params_def += f"""Params {value_names}_params = {{ {i}, NUM({value_names}),  {value_names} }};\n"""
    header_file.write(params_def)
    print(params_def)

    input_size = get_input_size(onnx_model)
    header_file.write(f"float input_holder[{input_size}]={{}};")

def get_input_size(onnx_model):
    dims = onnx_model.graph.input[0].type.tensor_type.shape.dim
    raw_dims = [x.dim_value for x in dims]
    return reduce((lambda x, y: x * y), raw_dims)

with open("remote_arduino_net/weight_definitions.h", "w") as param_file:
    make_param_definition_header(onnx_model, param_file)

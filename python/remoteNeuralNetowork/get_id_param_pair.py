def get_id_param_pair_iterator(onnx_model):
    return enumerate(onnx_model.graph.initializer)
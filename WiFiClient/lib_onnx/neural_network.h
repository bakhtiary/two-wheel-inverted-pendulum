struct TransferValues{
  int len;
  float * values;
  bool nearly_equals(float * other_values){
    for(int i = 0; i < len; i++){
      float diff = values[i] - other_values[i];
      if(diff > 0.0002 || diff < -0.0002){
        return false;
      }
    }
    return true;
  }
};

struct Stage{
  public:
  TransferValues * output;
  Stage(int output_size){
    output = new TransferValues{output_size, new float [output_size]};  
  }
  TransferValues * compute(TransferValues * input);
};

struct Params {

    int class_id;  
    int len;
    float * values;
};

struct FullyConnected: public Stage
{
  int input_size;
  Params & weights;
  Params & biases;
  
  FullyConnected(
    int output_size,
    Params & weights,
    Params & biases
  ): Stage(output_size), weights(weights), biases(biases){}

  TransferValues * compute(TransferValues * input){
    for (int i = 0; i < output->len; i++){
      output->values[i] = biases.values[i];
      for (int j = 0; j < input->len; j++){
        output->values[i] += input->values[j]*weights.values[j + i * input->len];
      }
    }
    return output;
  };

  
};

class Relu: public Stage{
  public:
  Relu(int output_size):Stage(output_size){}
  TransferValues * compute(TransferValues * input){
    for (int i = 0; i < input->len; i++){
      float cur_val = input->values[i];
      output->values[i] = cur_val < 0 ? 0 : cur_val;
    }
    return output;
  }
};

class Tanh: public Stage{
  public:
  Tanh(int output_size):Stage(output_size){}
  TransferValues * compute(TransferValues * input){
    return output;
  }
};


class NeuralNetwork{
  public:
  int len_stages;
  Stage * stages;
  TransferValues * compute(TransferValues * values){
    for (int i = 0; i < len_stages; i++){
      values = stages[i].compute(values);
    }
    return values;
  }
};

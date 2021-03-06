struct TransferValues{
  int len;
  float * values;
  TransferValues(int len, float * values):len(len), values(values){}
  
  bool nearly_equals(float * other_values){
    for(int i = 0; i < len; i++){
      float diff = values[i] - other_values[i];
      if(diff > 0.0002 || diff < -0.0002){
        return false;
      }
    }
    return true;
  }
  String toString(){
    String retval = String("len: ")+len+" values:";
    for(int i = 0; i < len; i++){
      retval += String(" ") + values[i] ;
    }
    return retval;
  }
  String toJson(){
    String retval = "[";
    for(int i = 0; i < len; i++){
      if (i > 0){
          retval += ","; 
      }
      if (isnan (values[i])){
          retval += "NaN";
      }else{
          retval += String(values[i]);
      }
    }
    retval += "]";
    return retval;
  }

  
  };


struct Stage{
  public:
  TransferValues * output;
  Stage(int output_size){
    output = new TransferValues{output_size, new float [output_size]};  
  }
  virtual TransferValues * compute(TransferValues * input) = 0;
  virtual ~Stage(){}
  
  virtual String toString(){
    return output->toString();
  };

};

struct Params {

    int class_id;  
    int len;
    float * values;
    String toString(){
    String retval = String("len: ")+len+" values:";
    for(int i = 0; i < len; i++){
      retval += String(" ") + values[i] ;
    }
    return retval;
  }
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
  ): Stage(output_size), weights(weights), biases(biases){
    input_size = weights.len / output_size;
  }

  TransferValues * compute(TransferValues * input){
    for (int i = 0; i < output->len; i++){
      output->values[i] = biases.values[i];
      for (int j = 0; j < input->len; j++){
        output->values[i] += input->values[j]*weights.values[j + i * input->len];       
      }
    }
    return output;
  };

  String toString(){
    String retval("weights: \n");
    for(int i = 0; i < output->len; i++){
      for (int j = 0; j < input_size; j++){
        retval += String(weights.values[j + i * input_size]) + " ";
      }
      retval += "\n";
    }
    retval += ("\n biases: \n");
    for(int i = 0; i < output->len; i++){
        retval += String(biases.values[i]) + " ";
    }
    retval += "\n" + output->toString();
    return retval;
  }
  
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
    for (int i = 0; i < input->len; i++){
      float cur_val = input->values[i];
      if (cur_val < -10){
        output->values[i] = -1;
      }else if(cur_val > 10){
        output->values[i] = 1;
      }else{
        float pos_exp = exp(cur_val);
        float neg_exp = exp(-cur_val);
        output->values[i] = (pos_exp - neg_exp)/(pos_exp + neg_exp);
      }
    }
    return output;
  }
};


class NeuralNetwork{
  public:
  int len_stages;
  Stage ** stages;
  TransferValues * compute(TransferValues * values){
    for (int i = 0; i < len_stages; i++){
      values = stages[i]->compute(values);
    }
    return values;
  }

  String toString(){
    String retval("");
    for (int i = 0; i < len_stages; i++){
      retval += stages[i]->toString();
    }
    return retval;
  }
};

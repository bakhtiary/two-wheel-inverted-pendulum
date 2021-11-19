
struct WeightGram: CommunicationData{
  int param_id;
  int start_loc;
  float x0, x1, x2, x3, x4, x5, x6, x7;
  WeightGram(int id=10, int param_id=0, int start_loc=0, float x0=0, float x1=0, float x2=0, float x3=0, float x4=0, float x5=0, float x6=0, float x7=0)
  :param_id(param_id),x0(x0), x1(x1), x2(x2), x3(x3), x4(x4), x5(x5), x6(x6), x7(x7)
  { this->id = id;}
  String toString(){
    return String("")+id+ " " + param_id + " " + x0 + " " + x2 + " ... " + x7;
  }
};

template <int EXTRA_PAYLOAD_LEN>
struct InputGram: CommunicationData{
  int float_payload_len=EXTRA_PAYLOAD_LEN;
  float payload[EXTRA_PAYLOAD_LEN];
  InputGram(int id=11,int float_payload_len=EXTRA_PAYLOAD_LEN){this->id = id;}
  String toString(){
    String retval = "";
    for(int i = 0; i < float_payload_len; i++){
      retval += payload[i];
      retval += " ";
    }
    return String("") + id + " len " + float_payload_len + " values " + retval;
  }
};

template <int EXTRA_PAYLOAD_LEN>
struct OutputGram: CommunicationData{
  int float_payload_len=EXTRA_PAYLOAD_LEN;
  float payload[EXTRA_PAYLOAD_LEN];
  OutputGram(int id=12,int float_payload_len=EXTRA_PAYLOAD_LEN){this->id = id;}
  String toString(){
    String retval = "";
    for(int i = 0; i < float_payload_len; i++){
      retval += payload[i];
      retval += " ";
    }
    return String("") + id + " len " + float_payload_len + " values " + retval;
  }
};

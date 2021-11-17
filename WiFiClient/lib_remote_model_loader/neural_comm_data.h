struct InputGram: CommunicationData{
  float x;
  float y;
  InputGram(int id=10,int x=2,int y=3){
    this->id = id;
    this->x = x;
    this->y = y;
  }
  String toString(){
    return String("")+id+ " " + x + " " + y + " " ;
  }
};

struct OutputGram: CommunicationData{
  float x;
  float y;
  OutputGram(int id=11,int x=2,int y=3){
    this->id = id;
    this->x = x;
    this->y = y;
  }
  String toString(){
    return String("")+id+ " " + x + " " + y + " " ;
  }
};


struct WeightGram: CommunicationData{
  int param_id;
  int start_loc;
  float x0, x1, x2, x3, x4, x5, x6, x7;
  WeightGram(int id=12, int param_id=0, int start_loc=0, float x0=0, float x1=0, float x2=0, float x3=0, float x4=0, float x5=0, float x6=0, float x7=0)
  :param_id(param_id),x0(x0), x1(x1), x2(x2), x3(x3), x4(x4), x5(x5), x6(x6), x7(x7)
  { this->id = id;}
  String toString(){
    return String("")+id+ " " + param_id + " " + x0 + " " + x2 + " ... " + x7;
  }
};


struct Data1: CommunicationData{
  int x;
  int y;
  int z;
  Data1(int id=1,int x=2,int y=3,int z=4){
    this->id = id;
    this->x = x;
    this->y = y;
    this->z = z;
  }
  String toString(){
    return String("")+id+ " " + x + " " + y + " " + z + " ";
  }
};

struct Data2: CommunicationData{
  int a;
  int b;
  int c;
  float d;
  Data2(int id=2, int a=3, int b=4, int c=5, float d=0.6):a(a),b(b),c(c),d(d){this->id = id;}
  String toString(){
    return String("")+id+ " " + a + " " + b + " " + c + " ";
  }

};

struct TimeData: CommunicationData{
  int passed_time;
  TimeData(int id=3, int passed_time=0):passed_time(passed_time){this->id = id;}
  String toString(){
    return String("")+id+ " " + passed_time + " ";
  }

};

template <int EXTRA_PAYLOAD_LEN>
struct VarData: CommunicationData{
  int float_payload_len=EXTRA_PAYLOAD_LEN;
  float payload[EXTRA_PAYLOAD_LEN];
  VarData(int id=4,int float_payload_len=EXTRA_PAYLOAD_LEN){this->id = id;}
  String toString(){
    String retval = "";
    for(int i = 0; i < float_payload_len; i++){
      retval += payload[i];
      retval += " ";
    }
    return String("") + id + " len " + float_payload_len + " values " + retval;
  }

};

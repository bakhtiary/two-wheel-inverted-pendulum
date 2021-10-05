struct CommunicationData{
  int id;
};


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
};

struct TimeData: CommunicationData{
  int passed_time;
  TimeData(int id=3, int passed_time=0):passed_time(passed_time){this->id = id;}
};

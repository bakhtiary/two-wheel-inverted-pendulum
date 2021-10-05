from construct import Container

from server.data_descriptors import DataDescriptors


def test_desc_inititalization():
    lines = get_lines()
    dd = DataDescriptors(lines)
    data = expand_short_data(b"\x01\x02\x03\x02\x03")

    res = dd.parse_incoming_data(data)

    assert str(res) == """ListContainer: 
    Container: 
        type = (enum) Data1 1
        data = Container: 
            id = 1
            x = 2
            y = 3
    Container: 
        type = (enum) Data2 2
        data = Container: 
            id = 2
            x = 3"""
    pass


def expand_short_data(short_data):
    data = b"".join([one_byte.to_bytes(4, "little") for one_byte in short_data])
    return data


def test_descriptor_for_building():
    lines = get_lines()
    dd = DataDescriptors(lines)
    data = Container(id=1, x=2, y=3)
    assert dd.build(data) == expand_short_data(b"\x01\x02\x03")



def get_lines():
    lines = """
struct Data1: CommunicationData{
  Data1(int id=1,int x=2,int y=3){
  }
};

struct Data2: CommunicationData{
  Data2(int id=2,int x=2){
  }
};


        """.split("\n")
    return lines

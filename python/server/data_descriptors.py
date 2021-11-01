import os
import re
from io import BytesIO

from construct import Struct, Int32ul, Float32l, Container, Enum, Switch, this, GreedyRange, Union
from dotenv import load_dotenv

load_dotenv()


class DataDescriptorsFactory:
    def __init__(self, filename):
        self.filename = filename

    def makeDD(self):
        lines = []
        with open(self.filename) as f:
            for line in f.readlines():
                lines.append(line)

        return DataDescriptors(lines=lines)


class DataDescriptors():
    def __init__(self, lines):

        self.bytes_remaining = b""
        self.id_maps_to_structs_container_name_tupple = read_structs(lines)
        type_names_to_ids = {val[2]: key for key, val in self.id_maps_to_structs_container_name_tupple.items()}
        type_names_to_structs = {val[2]: val[0] for key, val in self.id_maps_to_structs_container_name_tupple.items()}

        st = Union(1,
            "type" / Enum(Int32ul, **type_names_to_ids),
            "data" / Switch(this.type,
                            type_names_to_structs
                            ),
        )

        self.Construct = GreedyRange(st)
    def parse_incoming_data(self, incoming_data):

        byte_stream = BytesIO(self.bytes_remaining + incoming_data)
        request = self.Construct.parse_stream(byte_stream)
        self.bytes_remaining = byte_stream.read()
        return request

    def build(self, container):
        return self.id_maps_to_structs_container_name_tupple[container["id"]][0].build(container)


if __name__ == "__main__":
    DataDescriptorsFactory(f"{os.getenv('REPOSITORY_ROOT')}/WiFiClient/lib_remote_registry/remote_registry.h")


def read_structs(descriptor_lines):
    lines = descriptor_lines

    data_objects = []
    for line in lines:
        if "CommunicationData" in line:
            pattern = 'struct\s+(\w+)\s*:\s*CommunicationData\s*{'
            match = re.search(pattern, line)
            if (match):
                data_objects.append(match.group(1))
            else:
                #print("Nothing found on: " + line)
                pass

    id_maps_to_structs_container_name_tupple = {}
    for line in lines:
        for register_name in data_objects:
            if re.search(f"{register_name}.*\(.*\)", line):
                signature = line[line.find('(') + 1:line.find(')')]
                struct_params = []
                default_values = {}
                type_converters = {}
                current_id = None
                for part in signature.split(","):
                    match = re.search("\s*(\w+)\s+(\w+)\s*=\s*(\S+)", part)
                    if match:
                        type, var_name, value_string = match.groups()
                        if type == "int":
                            param = var_name / Int32ul #this / is overloaded and it is just the Renamed class from construct
                            value = int(value_string)
                            type_converter = int
                        elif type == "float":
                            param = var_name / Float32l #this / is overloaded and it is just the Renamed class from construct
                            value = float(value_string)
                            type_converter = float
                        else:
                            print(f"ERROR: could not understand {type} in part: {part} in line: {line}")
                            param = value = type_converter = None

                        if var_name == "id":
                            current_id = int(value)

                        struct_params.append(param)
                        default_values[var_name] = value
                        type_converters[var_name] = type_converter
                    else:
                        print(f"no match in part {part}")
                if current_id in id_maps_to_structs_container_name_tupple:
                    print(f"Warning replicated id: {current_id}")
                id_maps_to_structs_container_name_tupple[current_id] = (Struct(*struct_params), Container(**default_values), register_name, type_converters)

    return id_maps_to_structs_container_name_tupple
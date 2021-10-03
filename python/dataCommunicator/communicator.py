import re

class Communicator():
    def __init__(self, filename):
        lines = []
        with open(filename) as f:
            for line in f.readlines():
                lines.append(line)

        data_objects = []
        for line in lines:
            if "CommunicationData" in line:
                pattern = 'struct\s+(\w+)\s*:\s*CommunicationData\s*{'
                match = re.search(pattern, line)
                if(match):
                    data_objects.append(match.group(1))
                else:
                    print("Nothing found on: "+line)

        for line in lines:
            for name in data_objects:
                if re.search(f"{name}.*\(.*\)", line):
                    signature = line[line.find('(')+1:line.find(')')]
                    print(signature)
                    for part in signature.split(","):
                        print(part)







if __name__ == "__main__":
    Communicator("C:\\Users\\amir\\Desktop\\esp32robotCenter\\WiFiClient\\lib_remote_registry\\remote_registry.h")
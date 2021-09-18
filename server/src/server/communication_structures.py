from construct import Struct, Int32ul, Float32l

robot_read_format = Struct(
    "event_id" / Int32ul,
    "start_time" / Int32ul,
    "end_time" / Int32ul,
    "ax" / Float32l,
    "ay" / Float32l,
    "az" / Float32l,
    "gx" / Float32l,
    "gy" / Float32l,
    "gz" / Float32l,
)
robot_read_format2 = Struct(
    "event_id" / Int32ul,
    "start_time" / Int32ul,
    "end_time" / Int32ul,
    "power" / Float32l,
)
robot_write_format = Struct(
    "proportional" / Float32l,
    "offset" / Float32l,
    "delay_time" / Float32l,
)
robot_write_format2 = Struct(
    "proportional" / Float32l,
    "integration" / Float32l,
    "derivative" / Float32l,
    "minimal_motor_power" / Float32l,
    "offset" / Float32l,
    "delay_time" / Float32l,
)
test_read_format = Struct(
    "x" / Int32ul,
    "y" / Int32ul,
)
test_write_format = Struct(
    "x" / Int32ul,
    "y" / Float32l,
)
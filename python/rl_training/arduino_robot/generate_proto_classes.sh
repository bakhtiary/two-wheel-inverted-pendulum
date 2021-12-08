#!/bin/sh
protoc --python_out=.. robot_control.proto
protoc --nanopb_out=. robot_control.proto

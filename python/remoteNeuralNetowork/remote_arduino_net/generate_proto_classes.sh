#!/bin/sh
protoc --python_out=.. remote_network.proto
protoc --nanopb_out=. remote_network.proto

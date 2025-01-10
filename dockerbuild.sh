#!/bin/bash

docker build -t wahoo .

docker run -itd --name wahoo -p 8090:8090 wahoo
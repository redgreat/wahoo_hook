#!/bin/bash

docker build -t wahoo .

docker run -itd --name wahoo -p 8090:8090 wahoo

docker run -itd --name wahoo -p 8090:8090 \
  -v /vol1/1000/docker/wahoo/config:/code/app/config \
ghcr.io/redgreat/wahoo_webhook:latest
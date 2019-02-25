#!/bin/sh
docker run -v maki:/maki/persist --restart on-failure -t maki

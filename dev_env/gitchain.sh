#!/bin/bash
docker rm -f gitchain;
docker run \
--name gitchain \
-p 80:80 \
-v `pwd`/../:/app \
-it gitchain bash;

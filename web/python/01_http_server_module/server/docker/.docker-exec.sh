#!/bin/bash

docker exec -ti "$(docker ps | grep "web:1.0" | awk '{print $1}')" /bin/bash


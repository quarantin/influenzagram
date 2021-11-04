#!/bin/bash
cd $(dirname "${0}")

docker-compose -f docker-compose.yml exec app "./manage.py" "$@"
#docker-compose -f docker-compose.yml exec -T app "./manage.py" "$@"

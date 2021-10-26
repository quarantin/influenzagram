#!/bin/bash
set -e

cd $(dirname "${0}")

sudo apt -y update --fix-missing
sudo apt -y install mysql-server python3 python3-pip python3-setuptools redis-server

update-alternatives --install /usr/bin/python python /usr/bin/python3 1

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

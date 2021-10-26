#!/bin/bash

sudo /etc/init.d/mysql restart
sudo /etc/init.d/redis-server restart
python manage.py runserver

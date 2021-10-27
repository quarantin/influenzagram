# influenzagram

A tool to monitor people of influence

## Setup

* Install docker: https://docs.docker.com/engine/installation/
* Install docker-compose: https://docs.docker.com/compose/install/
* Build the docker image: `./docker-compose.sh build`
* Start the stack: `./docker-compose.sh up`
* Create database: `./django-manage.sh migrate`
* Create admin user: `./django-manage.sh createsuperuser --email admin@example.com --username admin`
* Your server is accessible at http://localhost/

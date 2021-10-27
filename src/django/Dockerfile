FROM ubuntu:20.04

RUN apt-get -y update --fix-missing
RUN apt-get -y install \
	python3 \
	python3-pip \
	python3-setuptools
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt


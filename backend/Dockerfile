FROM ubuntu:16.04

RUN echo "alias python=python3" >> ~/.bashrc
RUN echo "alias pip=python3" >> ~/.bashrc
RUN bash ~/.bashrc

RUN apt-get update && \
  apt-get install python3 -y && \
  apt-get install python3-pip -y

RUN pip3 install django pytest pytest-django pytest-cov mixer

RUN mkdir -p /code
ADD . /code
WORKDIR /code

EXPOSE 8000

CMD ['python3', 'manage.py', 'runserver']

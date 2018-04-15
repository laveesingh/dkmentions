FROM ubuntu:16.04

RUN echo "alias python=python3" >> ~/.bashrc
RUN echo "alias pip=python3" >> ~/.bashrc

RUN mkdir -p /code
ADD . /code
WORKDIR /code

RUN apt update && \
  apt install python3-pip && \
  pip install django && \
  pip install pytest && \
  pip install pytest-django && \
  pip install pytest-cov && \
  pip install mixer

EXPOSE 8000

CMD ['python', 'manage.py', 'runserver']

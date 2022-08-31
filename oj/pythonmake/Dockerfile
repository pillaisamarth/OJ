FROM python:latest

COPY . /usr/bin

WORKDIR /usr/bin

RUN sed -i -e 's/\r$//' python_ex.sh && sed -i -e 's/\r$//' iter.sh

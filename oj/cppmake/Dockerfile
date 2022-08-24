FROM gcc:latest


COPY . /usr/bin

WORKDIR /usr/bin

RUN apt-get update -y && apt-get install curl -y
RUN sed -i -e 's/\r$//' cpp_ex.sh && sed -i -e 's/\r$//' iter.sh

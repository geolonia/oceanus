FROM ubuntu:18.04
LABEL maintainer="ryo@geolonia.com"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    curl \
    git \
    bc \ 
    make \ 
    rename \
    python-pip \
    zlib1g \
    zlib1g-dev \
    libsqlite3-dev

RUN git clone git://github.com/mapbox/mbutil.git && \
    cd mbutil && \
    python setup.py install

RUN git clone https://github.com/mapbox/tippecanoe.git && \
    cd tippecanoe && \
    make -j && \
    make install    

COPY . /app

WORKDIR /root
FROM python:3.6.4-alpine3.7
COPY ./apk-repositories.txt /etc/apk/repositories
RUN apk update && apk add \
    gcc \
    g++ \
    make \
    cmake \
    zlib-dev \
    libc-dev \
    jpeg-dev \
    python3-dev \
&& pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
    face_recognition==1.2.3 \
    flask==1.0.2 \
    && apk del cmake gcc python3-dev make g++ \
    && apk add libstdc++

WORKDIR /opt/face
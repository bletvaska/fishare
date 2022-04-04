FROM alpine:edge

# metadata
LABEL maintainer="mirek <mirek@cnl.sk>"
LABEL title="Fishare"
LABEL description="File sharing service for my Microservices in Python course."
LABEL version="2022.01"

# set timezone
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Europe/Bratislava /etc/localtime \
    && echo "Europe/Bratislava" > /etc/timezone \
    && apk del tzdata 

# install poetry
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk update \
    && apk add --no-cache py3-pip curl

# set aplication workdir
WORKDIR /app

# copy and install project/application
ARG PACKAGE=fishare-2022.1-py3-none-any.whl

COPY dist/$PACKAGE /app
RUN pip3 install --no-cache-dir /app/$PACKAGE \
    && rm /app/$PACKAGE

# set healthcheck
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost/healthz || exit 1

# volumes
VOLUME /app/data/database.db
VOLUME /app/data/storage/

# run
CMD ["uvicorn", "fishare.main:app", "--host", "0.0.0.0", "--port", "80"]


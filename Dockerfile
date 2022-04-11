FROM alpine AS builder
LABEL mainter "mirek <mirek@cnl.sk>"

RUN apk add \
    py3-pip \
    gcc \
    python3-dev \
    musl-dev \
    alpine-sdk \
    && mkdir /wheels

COPY dist/fishare-0.1.0-py3-none-any.whl /wheels/

RUN pip install wheel \
    && pip wheel --wheel-dir=/wheels/ \
       /wheels/fishare-0.1.0-py3-none-any.whl 


FROM alpine AS base
LABEL mainter "mirek <mirek@cnl.sk>"

COPY --from=builder /wheels/*whl /tmp/

RUN apk add py3-pip \
    && cd /tmp/ \
    && pip install *whl \
    && pip cache purge \
    && rm -rf *whl \
    && mkdir -p /app/storage

EXPOSE 8000
VOLUME /app/storage

WORKDIR /app

CMD [ "fishare" ]

FROM python:3.10-slim-bullseye
LABEL maintainer="mirek <mirek@cnl.sk>"

COPY dist/fishare-0.1.0-py3-none-any.whl /tmp/

RUN cd /tmp/ \
    && pip install ./fishare*whl \
    && pip cache purge \
    && rm -rf *whl \
    && mkdir -p /app/storage

EXPOSE 8000
VOLUME /app/storage

WORKDIR /app

CMD [ "fishare" ]

FROM python:3.10-slim-bullseye
LABEL maintainer="mirek <mirek@cnl.sk>"

RUN adduser --no-create-home --disabled-password --gecos "" appuser

COPY dist/fishare-0.1.0-py3-none-any.whl /tmp/

RUN cd /tmp/ \
    && apt update && apt install -y curl \
    && pip install ./fishare*whl \
    && pip cache purge \
    && rm -rf *whl \
    && mkdir -p /app/storage \
    && chown -R appuser.appuser /app/storage


HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
VOLUME /app/storage

WORKDIR /app
USER appuser

CMD [ "fishare" ]

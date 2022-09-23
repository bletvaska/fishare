FROM python:3.10-slim
LABEL maintainer "mirek <mirek@cnl.sk>"

RUN adduser --no-create-home --disabled-password --gecos "" appuser

COPY dist/fishare-0.9.0-py3-none-any.whl /tmp/

RUN pip install /tmp/fishare-0.9.0-py3-none-any.whl \
    && pip cache purge \
    && rm /tmp/*whl \
    && mkdir -p /app/storage \
    && chown -R appuser.appuser /app

USER appuser
WORKDIR /app

EXPOSE 8000
VOLUME /app/storage/

CMD [ "fishare" ]


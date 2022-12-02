FROM python:3.11-slim
LABEL maintainer="mirek <mirek@cnl.sk>"

RUN adduser --no-create-home --disabled-password --gecos "" appuser

COPY dist/fishare-0.2.0-py3-none-any.whl /tmp/

RUN pip install --upgrade pip \
    && pip install /tmp/fishare-0.2.0-py3-none-any.whl \
    && rm /tmp/*whl \
    && pip cache purge \
    && mkdir -p /app/storage \
    && chown -R appuser.appuser /app

WORKDIR /app

EXPOSE 9000
VOLUME /app/storage/
USER appuser

CMD [ "python", "-m", "fishare.main" ]

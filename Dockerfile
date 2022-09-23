FROM python:3.10-slim
LABEL maintainer="mirek <mirek@cnl.sk>"

RUN adduser --no-create-home --disabled-password --gecos "" appuser

COPY dist/fishare-0.9.0-py3-none-any.whl /tmp/

RUN pip install /tmp/fishare-0.9.0-py3-none-any.whl httpie \
    && pip cache purge \
    && rm /tmp/*whl \
    && mkdir -p /app/storage \
    && chown -R appuser.appuser /app \
    && apt update && apt install -y curl \
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
    CMD http get http://localhost:8000/health/ --check-status || exit 1
    #CMD curl -f http://localhost:8000/health/ || exit 1

USER appuser
WORKDIR /app

EXPOSE 8000
VOLUME /app/storage/

CMD [ "fishare" ]


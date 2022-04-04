FROM python:slim-bullseye

# poetry build
COPY dist/fishare-2022.1-py3-none-any.whl /tmp/

RUN pip install /tmp/fishare-2022.1-py3-none-any.whl \
    && rm /tmp/fishare-2022.1-py3-none-any.whl

EXPOSE 80
# fixme kery priecinok je storage?
VOLUME /storage

# run container as specific user
# healthcheck
# what is the time? / timezone
# security scan/check

CMD [ "uvicorn", "fishare.main:app", "--host", "0.0.0.0", "--port", "80" ]
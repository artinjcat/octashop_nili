FROM python:3.13-alpine

COPY requirements /requirements
COPY scripts /scripts
COPY src /src

WORKDIR /src

EXPOSE 8000

RUN python -m pip install --no-cache-dir -r /requirements/deployment.txt

RUN chmod -R +x /scripts && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    adduser --disabled-password --no-create-home octashop && \
    chown -R octashop:octashop /vol && \
    chmod -R 755 /vol

ENV PATH="/scripts:$PATH"

USER octashop

CMD ["run.sh"]
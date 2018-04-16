ARG PY_VERSION="3.5"
ARG DIST="slim"

FROM python:${PY_VERSION}-${DIST}
WORKDIR /jupyxplorer
ADD . .

RUN pip install -U pip && \
    pip install . && \
    rm -rf /root/.cache
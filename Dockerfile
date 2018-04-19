ARG PY_VERSION="3.5"
ARG DIST="slim"

FROM python:${PY_VERSION}-${DIST}
WORKDIR /jupyxplorer

COPY requirements*.txt ./

RUN pip install -U pip && \
    pip install -r requirements.txt

ADD . .

RUN pip install . && \
    rm -rf /root/.cache

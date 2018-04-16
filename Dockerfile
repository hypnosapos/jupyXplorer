ARG PY_VERSION="3.5"
ARG DIST="slim"

FROM python:${PY_VERSION}-${DIST}
COPY requirements.txt .
RUN pip install -U pip &&\
    pip install -r requirements.txt

FROM python:${PY_VERSION}-${DIST}
COPY --from=0 /root/.cache /root/.cache

WORKDIR /jupyxplorer

ADD . .

RUN pip install -U pip && pip install . && \
    rm -rf /root/.cache
# Basic Dockerfile for a Flask application

# Alpine is smaller and more security focused than the ubuntu base
FROM python:3.6-alpine

ENV FLASK_APP my_library.main

ARG DEPLOY_ENVIRONMENT=dev

COPY . /build

WORKDIR /build

RUN pip install setuptools wheel

RUN if [[ "$DEPLOY_ENVIRONMENT" == "dev" ]]; then \
        pip install -e . ; \
    else \
        python setup.py bdist_wheel && \
        pip install dist/* && \
        rm -rf ./* \
    fi

WORKDIR /

RUN ["flask", "run"]

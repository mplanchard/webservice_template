# Basic Dockerfile for a Flask application

# Alpine is smaller and more security focused than the ubuntu base
FROM python:3.6-alpine

ENV FLASK_APP my_library.main

ARG DEPLOY_ENVIRONMENT=dev

COPY . /build

WORKDIR /build

RUN apk add --no-cache build-base postgresql-dev && \
    pip install setuptools wheel && \
    if [[ "$DEPLOY_ENVIRONMENT" == "dev" ]]; then \
        pip install -e . ; \
    else \
        python setup.py bdist_wheel && \
        pip install dist/* && \
        rm -rf ./* ; \
    fi && \
    apk del build-base

WORKDIR /

CMD ["flask", "run", "--host=0.0.0.0"]

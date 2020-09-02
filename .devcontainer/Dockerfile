# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.8"

FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

COPY requirements.txt /tmp/
COPY requirements-dev.txt /tmp/

RUN pip3 --no-cache-dir install -U pip \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-dev.txt \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt


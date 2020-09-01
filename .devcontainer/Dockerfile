# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.134.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3.8"

FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT} as builder

COPY Pipfile* ./

RUN pip3 install -U pip \
    && pip3 install pipenv \
    && pipenv lock --requirements > /tmp/requirements.txt \
    && pipenv lock --dev --requirements > /tmp/requirements-dev.txt

FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

COPY --from=builder /tmp/requirements.txt /tmp/
COPY --from=builder /tmp/requirements-dev.txt /tmp/

RUN pip3 --no-cache-dir install -U pip \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements-dev.txt \
    && pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt


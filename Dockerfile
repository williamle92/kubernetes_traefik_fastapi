# syntax=docker/dockerfile:1

FROM python:3.11.9-slim-bookworm as Base
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app

# Copy the source code into the container.
COPY . .

RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=api/requirements.txt,target=api/requirements.txt \
    python -m pip install -r api/requirements.txt


# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.


# Switch to the non-privileged user to run the application.
USER appuser


# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uvicorn api.backend.main:app --reload --host 0.0.0.0

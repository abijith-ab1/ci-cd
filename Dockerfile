# base image
FROM python:3.10-slim


# set workdir
WORKDIR /app


# install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
libpq-dev \
gcc \
&& rm -rf /var/lib/apt/lists/*


# copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt


# copy project
COPY . /app


# collect static in container (run at build or entrypoint)
ENV DJANGO_SETTINGS_MODULE=config.settings


# port
EXPOSE 8000


# entrypoint command (gunicorn)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
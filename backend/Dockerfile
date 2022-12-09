FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip3 install -r /app/requirements.txt --no-cache-dir && \
    python /app/manage.py collectstatic --noinput
CMD python /app/manage.py migrate && \
    gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

FROM python:3.11-alpine

WORKDIR /app

COPY requirements/prod.txt /tmp/requirements
RUN pip install --no-cache-dir -r /tmp/requirements

COPY shopeat /app/shopeat
ENTRYPOINT [ "python", "-m", "shopeat" ]

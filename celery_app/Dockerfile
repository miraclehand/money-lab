FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY packages /app/packages
RUN pip install /app/packages/*.whl

COPY . /app


FROM python:3.11-slim

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY packages /app/packages
RUN pip install /app/packages/*.whl

COPY . /app

#CMD ["python", "main.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8081", "--reload", "app:run_app"]

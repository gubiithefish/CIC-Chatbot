FROM python:3.8

COPY . /app
COPY requirements.txt /app
WORKDIR /app

RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

USER root

EXPOSE 8000



CMD ["python3", "-m", "uvicorn", "--host", "0.0.0.0", "server.main:app"]
#CMD ["python3", "./server/main.py", "start"]

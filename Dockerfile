FROM python:3.8

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app

WORKDIR /app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

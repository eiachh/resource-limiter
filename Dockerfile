FROM python:latest

ENV resource_limiter_port=5000
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app
ADD . /app
WORKDIR /app

EXPOSE 5000

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

RUN export FLASK_APP=main.py
CMD ["python", "./main.py"]
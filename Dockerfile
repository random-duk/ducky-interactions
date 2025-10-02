from python:3.12-slim

RUN apt-get update && apt-get install -y procps gcc
WORKDIR /app
copy requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

ENTRYPOINT ["bash", "start.sh"]
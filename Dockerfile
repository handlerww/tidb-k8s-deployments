FROM python:3.6-slim

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./

EXPOSE 5000
CMD ["python", "index.py"]
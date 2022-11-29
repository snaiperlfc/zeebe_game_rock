FROM python:3.9-alpine
RUN apk add --update --no-cache py-pip build-base  linux-headers libxslt-dev
RUN mkdir /app

COPY requirements.txt /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt  \
&& apk del build-base linux-headers py-pip \
&& apk add libpq && rm -rf /var/cache/apk/* \
&& find / -name "*.pyc" -delete && find / -name "*.o" -delete

COPY / /app

CMD ["python3", "/app/main.py"]

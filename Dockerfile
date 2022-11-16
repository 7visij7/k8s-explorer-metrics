FROM python:3.6-alpine
WORKDIR /opt/
COPY . .
COPY requirements.txt .
RUN apk add --virtual .deps gcc openssl-dev python3-dev make linux-headers musl-dev libffi-dev curl fcgi
RUN pip3 install -r requirements.txt
CMD ["python3", "-m", "explorer"]
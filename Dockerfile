FROM python:3.8-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY FlaskApp /app
WORKDIR /app


COPY entrypoint.sh /entrypoint.sh

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]

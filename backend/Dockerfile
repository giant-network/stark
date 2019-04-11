FROM python:3.6

COPY . ./stark

WORKDIR stark

RUN  apt-get update -y && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev && pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "6", "--timeout", "60", "--log-level", "DEBUG", "-k", "gevent", "wsgi:application"]
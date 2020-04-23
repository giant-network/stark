FROM python:3.6

COPY . ./stark

WORKDIR stark

RUN cd /stark/backend && apt-get update -y && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev nginx && pip install -r requirements.txt

RUN mv stark_nginx.conf /etc/nginx/conf.d/

EXPOSE 8080

CMD ["sh", "run.sh"]
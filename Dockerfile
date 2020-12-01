# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.7-buster
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
#copy certs
COPY self-signed-certs/mcs.crt /etc/nginx/mcs.crt
COPY self-signed-certs/mcs.key /etc/nginx/mcs.key
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/minesCrowdsourcing
COPY requirements.txt start-server.sh /opt/app/
COPY minesCrowdsourcing /opt/app/minesCrowdsourcing/
RUN ls /opt/app/minesCrowdsourcing
WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN chmod 664 /opt/app/minesCrowdsourcing/db.sqlite3
RUN chown -R www-data:www-data /opt/app
EXPOSE 9601
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]


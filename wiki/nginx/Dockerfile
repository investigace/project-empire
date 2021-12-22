FROM nginx:1.21

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

COPY localhost-selfsigned.crt /etc/ssl/certs/localhost-selfsigned.crt
COPY localhost-selfsigned.key /etc/ssl/certs/localhost-selfsigned.key

WORKDIR /app

CMD ["nginx", "-g", "daemon off;"]

FROM certbot/certbot:v1.22.0

# Add bash as we use it for running start.sh
RUN apk add bash

# Copy over start.sh and make it runnable
COPY start.sh /opt/certbot/start.sh
RUN chmod +x /opt/certbot/start.sh

ENTRYPOINT /opt/certbot/start.sh

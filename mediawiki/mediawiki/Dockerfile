FROM mediawiki:1.37

# Netcat is needed for wait-for to run
RUN apt-get -q update && apt-get -qy install netcat

COPY start.sh /root/start.sh
COPY wait-for /root/wait-for

RUN chmod +x /root/start.sh
RUN chmod +x /root/wait-for

RUN mkdir -p /opt/mediawiki_shared

RUN rm -r /var/www/html/images

RUN ln -s /opt/mediawiki_shared/images /var/www/html/images

RUN ln -s /opt/mediawiki_shared/LocalSettings.php /var/www/html/LocalSettings.php

CMD ["apache2-foreground"]

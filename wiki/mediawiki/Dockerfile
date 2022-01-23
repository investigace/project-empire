FROM mediawiki:1.37

# Netcat is needed for wait-for to run
RUN apt-get -q update && apt-get -qy install netcat

# Add start script
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh

# Add wait-for script
COPY wait-for /root/wait-for
RUN chmod +x /root/wait-for

# Add extensions
COPY extensions/EmbedVideo-e1e965 /var/www/html/extensions/EmbedVideo
COPY extensions/Iframe-v0.09 /var/www/html/extensions/Iframe

# Create directory shared with host system
RUN mkdir -p /opt/mediawiki_shared
RUN rm -r /var/www/html/images
RUN ln -s /opt/mediawiki_shared/images /var/www/html/images
RUN ln -s /opt/mediawiki_shared/public /var/www/html/public
RUN ln -s /opt/mediawiki_shared/LocalSettings.php /var/www/html/LocalSettings.php

# Add logo and install pages
COPY project_empire_wiki_logo.svg /var/www/html/public/project_empire_wiki_logo.svg
COPY install_pages /root/install_pages

CMD ["apache2-foreground"]

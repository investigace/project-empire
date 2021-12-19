FROM mediawiki:1.37

RUN mkdir -p /opt/mediawiki_shared

RUN rm -r /var/www/html/images

RUN ln -s /opt/mediawiki_shared/images /var/www/html/images

RUN ln -s /opt/mediawiki_shared/LocalSettings.php /var/www/html/LocalSettings.php

CMD ["apache2-foreground"]

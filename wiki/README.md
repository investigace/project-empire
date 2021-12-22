# Empire MediaWiki

In development

```
$ docker compose up
```

In production

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

On first run, nginx will use self-signed certificates for https, because
certificates have not yet been obtained from Lets Encrypt. Certbot will
obtain those certificates on first run, so you have to make sure to restart
nginx service to have it load the Lets Encrypt certificates.

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml restart nginx
```

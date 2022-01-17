FROM alpine:3.15

RUN \
	mkdir -p /aws && \
	apk -Uuv add groff less python3 py3-pip bash mariadb-client && \
	pip3 install awscli && \
	apk --purge -v del py-pip && \
	rm /var/cache/apk/*

COPY start.sh /

RUN \
  chmod +x /start.sh

ENTRYPOINT /start.sh

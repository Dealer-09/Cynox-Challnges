FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    nginx php8.1-fpm --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY web/index.php    /var/www/html/index.php
COPY web/welcome.html /var/www/html/welcome.html
COPY web/default.conf /etc/nginx/sites-available/default

RUN echo "cyn0x{lf1_l0g_p01s0n_w4k4nd4_f0r3v3r}" > /flag.txt && chmod 444 /flag.txt

# nginx needs to write access.log
RUN mkdir -p /var/log/nginx && chmod 755 /var/log/nginx

RUN cat > /start.sh << 'SH'
#!/bin/bash
service php8.1-fpm start
nginx -g "daemon off;"
SH
RUN chmod +x /start.sh

EXPOSE 80
CMD ["/start.sh"]
FROM php:8.1-apache

COPY web/ /var/www/html/

RUN echo "cyn0x{3num3r4t10n_1s_k3y_4g3nt}" > /flag.txt && \
    chmod 444 /flag.txt && \
    a2enmod rewrite

EXPOSE 80
CMD ["apache2-foreground"]
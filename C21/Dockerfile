FROM php:8.1-apache
COPY web/ /var/www/html/
RUN mkdir -p /var/www/html/themes && chmod 777 /var/www/html/themes
RUN echo "cyn0x{ph4r_byp4ss_0n_4sg4rd}" > /flag.txt && chmod 444 /flag.txt
RUN a2enmod rewrite
EXPOSE 80
CMD ["apache2-foreground"]
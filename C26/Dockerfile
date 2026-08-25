FROM php:8.1-apache

# Copy web files
COPY web/ /var/www/html/
COPY docker/000-default.conf /etc/apache2/sites-available/000-default.conf

# Create uploads directory
RUN mkdir -p /var/www/html/uploads && \
    chmod 777 /var/www/html/uploads

# Plant the flag
RUN echo "cyn0x{ph3_upl04d_f1lt3r_3vas10n}" > /flag.txt && \
    chmod 444 /flag.txt

# Enable mod_rewrite
RUN a2enmod rewrite

EXPOSE 80
CMD ["apache2-foreground"]
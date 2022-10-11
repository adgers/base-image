FROM php:7.1.33-fpm

COPY sources.list /etc/apt/
RUN apt-get update -y \
&& apt-get install -y nginx net-tools telnet procps
ENV PHP_CPPFLAGS="$PHP_CPPFLAGS -std=c++11"
RUN docker-php-ext-install pdo_mysql \
&& docker-php-ext-install opcache \
&& apt-get install libicu-dev -y \
&& docker-php-ext-configure intl \
&& docker-php-ext-install intl \
&& pecl install redis \
&& docker-php-ext-enable redis.so \
&& apt-get install libpng libpng-devel -y \ 
&& docker-php-ext-install gd && docker-php-ext-enable gd \
&& apt-get remove libicu-dev icu-devtools -y 

RUN { \
echo 'opcache.memory_consumption=128'; \
echo 'opcache.interned_strings_buffer=8'; \
echo 'opcache.max_accelerated_files=4000'; \
echo 'opcache.revalidate_freq=2'; \
echo 'opcache.fast_shutdown=1'; \
echo 'opcache.enable_cli=1'; \
} > /usr/local/etc/php/conf.d/php-opocache-cfg.ini

RUN apt-get install tzdata \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

COPY nginx.conf /etc/nginx/
COPY php-nginx.conf /etc/nginx/conf.d/
COPY run.sh /etc/run.sh
#COPY --chown=www-data:www-data . /var/www/html
WORKDIR /var/www/html
EXPOSE 80 9000 
RUN chmod +x /etc/run.sh

ENTRYPOINT ["/etc/run.sh"]

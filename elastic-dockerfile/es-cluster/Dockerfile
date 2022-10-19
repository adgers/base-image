FROM dockerproxy.com/bitnami/elasticsearch:7.16.3-debian-10-r2

RUN elasticsearch-plugin install https://ghproxy.com/https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.16.3/elasticsearch-analysis-ik-7.16.3.zip \
    && elasticsearch-plugin install analysis-icu \
    && elasticsearch-plugin install analysis-pinyin \
    && elasticsearch-plugin install analysis-poisson 

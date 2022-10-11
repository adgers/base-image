FROM registry.cn-chengdu.aliyuncs.com/images-a/es:analysis-7.16.3-analysis-icu



ADD  repository-s3 /usr/share/elasticsearch/plugins/repository-s3

RUN echo "-Des.allow_insecure_settings=true" >> /usr/share/elasticsearch/config/jvm.options


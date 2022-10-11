FROM fluentd:v1.14-1

USER root
RUN fluent-gem install fluent-plugin-elasticsearch \
    && fluent-gem install fluent-plugin-kafka
USER fluent

# https://github.com/elastic/elasticsearch-docker
FROM docker.elastic.co/elasticsearch/elasticsearch:7.5.2

RUN rm /usr/share/elasticsearch/config/elasticsearch.yml
COPY elasticsearch.yml /usr/share/elasticsearch/config/

# Add your elasticsearch plugins setup here
# Example: RUN elasticsearch-plugin install analysis-icu
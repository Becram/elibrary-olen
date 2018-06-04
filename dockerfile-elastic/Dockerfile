FROM elasticsearch:5.6.8

COPY elasticsearch.yml  /etc/elasticsearch/elasticsearch.yml

#Set timezone
ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#RUN sysctl -w vm.max_map_count=262144

WORKDIR /etc/elasticsearch

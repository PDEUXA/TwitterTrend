FROM apache/nifi-registry:latest
USER root
RUN apt-get update \
    && apt-get install -y ssh netcat rsync nano\
    && apt-get clean \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*
USER nifi
EXPOSE 18080
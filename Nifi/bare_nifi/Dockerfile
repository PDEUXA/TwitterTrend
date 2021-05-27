FROM apache/nifi:latest
USER root
RUN apt-get update \
    && apt-get install -y ssh netcat rsync nano python3 python3-pip\
    && apt-get clean \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install requests bs4
USER nifi

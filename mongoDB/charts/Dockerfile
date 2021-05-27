FROM quay.io/mongodb/charts:19.12.2

RUN apt-get update

ARG EMAIL
ARG PASSWORD

ENV EMAIL=${EMAIL} \
    PASSWORD=${PASSWORD}

COPY entrypoint.sh /usr/bin

ENTRYPOINT [ "entrypoint.sh" ]
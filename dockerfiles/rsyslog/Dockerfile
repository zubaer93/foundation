#########################################
# Rsyslog
#########################################
FROM alpine:3.9

# Install packages
# RUN apk add --update rsyslog && rm -rf /var/cache/apk/*
RUN apk add --no-cache rsyslog

# install configuration files
COPY rsyslog.conf /etc/rsyslog.conf

# Expose rsyslog port
EXPOSE 514 514/udp

# VOLUME [ "/var/log" ]

ENTRYPOINT ["rsyslogd", "-n", "-f", "/etc/rsyslog.conf"]


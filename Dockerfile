FROM wise2c/weblogic:1036

MAINTAINER Alan Peng <alan_peng@wise2c.com>

USER root

ENV CONFIG_JVM_ARGS '-Djava.security.egd=file:/dev/./urandom'

#Add weblogic scripts
ADD create-wls-domain.py /root/Oracle
ADD create_managed_server.py /root/Oracle
ADD ManagedServer.properties /root/Oracle
ADD register_managed_server.sh /root/Oracle

#Add entrypoint script
ADD entrypoint.sh /

#RUN mv create-wls-domain.py /root/Oracle && \
#         chmod +x /root/Oracle/create-wls-domain.py && \
#         chmod +x /entrypoint.sh

WORKDIR /root/Oracle/Middleware

ENV PATH $PATH:/root/Oracle/Middleware/wlserver_10.3/common/bin:/root/Oracle/Middleware/user_projects/domains/base_domain/bin

CMD ["/entrypoint.sh"]

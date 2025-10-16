FROM ghcr.io/jcroots/devops/aws:latest

LABEL maintainer="Jeremías Casteglione <jeremias.casteglione@rootstrap.com>"
LABEL version="251016"

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ARG ADMIN_UID=501
ARG ADMIN_GID=20

ENV ADMIN_UID=${ADMIN_UID}
ENV ADMIN_GID=${ADMIN_GID}

RUN groupadd -o -g ${ADMIN_GID} admin \
	&& useradd -o -d /home/admin -m -c 'admin' -g ${ADMIN_GID} -u ${ADMIN_UID} admin \
	&& chmod -v 0750 /home/admin

RUN printf 'umask %s\n' '027' >>/home/admin/.profile
RUN printf "export PS1='%s '\n" '\u@\h:\W\$' >>/home/admin/.profile

USER admin:admin
WORKDIR /home/admin

ENV USER=admin
ENV HOME=/home/admin

ENTRYPOINT ["/usr/local/bin/user-login.sh"]

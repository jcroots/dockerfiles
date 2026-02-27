FROM ghcr.io/jcroots/devops/gcloud:latest

LABEL maintainer="Jeremías Casteglione <jeremias.casteglione@rootstrap.com>"
LABEL version="260227"

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ARG ADMIN_UID=501
ARG ADMIN_GID=20

ENV ADMIN_UID=${ADMIN_UID}
ENV ADMIN_GID=${ADMIN_GID}

RUN groupadd -o -g ${ADMIN_GID} admin \
	&& useradd -o -d /home/admin -m -c 'admin' -g ${ADMIN_GID} \
		-u ${ADMIN_UID} admin \
	&& chmod -v 0750 /home/admin

RUN echo 'source /usr/local/etc/devops.bashrc' >>/home/admin/.profile

USER admin:admin
WORKDIR /home/admin

ENV USER=admin
ENV HOME=/home/admin

RUN install -v -d -m 0750 ${HOME}/.config \
	&& install -v -d -m 0750 ${HOME}/.config/gcloud

ENTRYPOINT ["/usr/local/bin/user-login.sh"]

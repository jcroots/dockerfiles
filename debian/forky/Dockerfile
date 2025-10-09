FROM debian:forky-20250929-slim

LABEL maintainer="Jeremías Casteglione <jeremias.rootstrap@gmail.com>"
LABEL version="251009"

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ENV DEBIAN_FRONTEND=noninteractive

ENV APT_INSTALL='bash bash-completion openssl ca-certificates media-types less wget sudo'

RUN apt-get clean \
	&& apt-get update -yy \
	&& apt-get dist-upgrade -yy --purge \
	&& apt-get install -yy --no-install-recommends ${APT_INSTALL} \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin

ARG JRMS_UID=501
ARG JRMS_GID=20

ENV JRMS_UID=${JRMS_UID}
ENV JRMS_GID=${JRMS_GID}

RUN groupadd -o -g ${JRMS_GID} jrms \
	&& useradd -o -d /home/jrms -m -c 'Jeremias' -g ${JRMS_GID} -u ${JRMS_UID} jrms \
	&& chmod -v 0750 /home/jrms

RUN printf 'umask %s\n' '027' >>/home/jrms/.profile
RUN printf "export PS1='%s '\n" '\u@\h:\W\$' >>/home/jrms/.profile

RUN echo 'jrms ALL=(ALL:ALL) NOPASSWD: ALL' >>/etc/sudoers.d/jrms
RUN chmod -v 0440 /etc/sudoers.d/jrms

COPY user-login.sh /usr/local/bin/user-login.sh
RUN chmod -v 0755 /usr/local/bin/user-login.sh

USER jrms:jrms
WORKDIR /home/jrms

ENV USER=jrms
ENV HOME=/home/jrms

ENTRYPOINT ["/usr/local/bin/user-login.sh"]

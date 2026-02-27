FROM jcroots/forky

LABEL maintainer="Jeremías Casteglione <jeremias.rootstrap@gmail.com>"
LABEL version="260227"

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ENV DEBIAN_FRONTEND=noninteractive

COPY apt.install /tmp/apt.install

RUN apt-get clean \
	&& apt-get update -yy \
	&& cat /tmp/apt.install | xargs apt-get install -yy --no-install-recommends \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin

ARG USER_NAME=jcroots

ENV USER_NAME=${USER_NAME}

COPY bashrc.brew /tmp/bashrc.brew
RUN install -v -m 0640 -o ${USER_NAME} -g ${USER_NAME} \
	/tmp/bashrc.brew /home/${USER_NAME}/.bashrc.brew
RUN printf 'source /home/%s/.bashrc.brew' "${USER_NAME}" >>"/home/${USER_NAME}/.profile"

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

ENV NONINTERACTIVE=1
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

ENV PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin

RUN brew update \
	&& brew install ca-certificates \
	&& brew cleanup --prune=all

ENTRYPOINT ["/usr/local/bin/user-login.sh"]

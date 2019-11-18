FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG="en_US.UTF-8" \
    LC_COLLATE="C" \
    LC_ALL="en_US.UTF-8" \
    PYENV_ROOT="/.pyenv" \
    PATH="/.pyenv/bin:/.pyenv/shims:$PATH" \
    TERM="xterm-256color"

RUN set -eux \
    && apt-get update \
    # Common build deps
    && apt-get install -y --no-install-recommends locales git curl ca-certificates \
    # Setup locales
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    # Get Pyenv installer
    &&  curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash  \
    # Pyenv build dependencies
    && apt-get install -y --no-install-recommends \
    make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev libpq-dev  \
    # Cleanup
    && apt-get purge -y --auto-remove curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY python-versions.txt ./

RUN set -eux \
    && pyenv update \
    && xargs -n 1 pyenv install < python-versions.txt \
    && pyenv global $(pyenv versions --bare) \
    && mv -v -- /python-versions.txt $PYENV_ROOT/version

WORKDIR /app

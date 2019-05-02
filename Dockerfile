FROM ubuntu:19.04

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME       /usr/lib/jvm

RUN  apt-get update && apt-get upgrade -y
RUN  apt-get install -y software-properties-common apt-utils net-tools
RUN  apt-get install -y --fix-missing locales curl python3-pip unzip tmux vim
# Set the locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Java 8
COPY binaryninja/jdk-8u211-linux-x64.tar.gz /tmp/jdk-8u211-linux-x64.tar.gz
RUN curl -fL https://raw.githubusercontent.com/chrishantha/install-java/master/install-java.sh -o /tmp/install-java.sh &&\
    chmod +x /tmp/install-java.sh &&\
    yes| /tmp/install-java.sh -f /tmp/jdk-8u211-linux-x64.tar.gz

# Grakn
COPY requirements.txt /tmp/requirements.txt
RUN  BROWSER_DOWNLOAD_URL=$(curl --silent https://api.github.com/repos/graknlabs/grakn/releases/latest | python3 -c "import sys; from json import loads as l; x = l(sys.stdin.read()); print(''.join(s['browser_download_url'] for s in x['assets'] if 'grakn-core-all-linux' in s['browser_download_url']))"); \
     curl -fL $BROWSER_DOWNLOAD_URL -o /tmp/grakn.tar.gz && \
     tar -C /opt -zxf /tmp/grakn.tar.gz && rm /tmp/grakn.tar.gz && \
     ln -s /opt/grakn*/grakn /usr/local/bin/ && ln -s /opt/grakn*/graql /usr/local/bin/ && \
     pip3 install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Binary Ninja
COPY binaryninja/BinaryNinja.zip /tmp/BinaryNinja.zip
RUN  unzip /tmp/BinaryNinja.zip -d /opt/ && rm /tmp/BinaryNinja.zip && \
     mkdir -p /root/.local/lib/python3.7/site-packages/ && \
     echo "/opt/binaryninja/python" > /root/.local/lib/python3.7/site-packages/binaryninja.pth && \
     mkdir -p /root/.binaryninja/
COPY binaryninja/license.txt /root/.binaryninja/license.dat
COPY binaryninja/update_to_version.py /opt/binaryninja/update_to_version.py

ENTRYPOINT ["bash"]

# && cd /opt/papermachete && python3 paper_machete.py
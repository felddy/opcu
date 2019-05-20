FROM python:3
MAINTAINER Mark Feldhousen <markf+opc@geekpad.com>

ARG OPC_UID=421
ARG INSTALL_IPYTHON="Yes Please"
ARG OPC_SRC="/usr/src/"
ENV OPC_HOME="/home/opc"

# OPC_YML can be set to point to a config file

RUN groupadd --system -g ${OPC_UID} opc && useradd -m --system -u ${OPC_UID} --gid opc opc

RUN if [ -n "${INSTALL_IPYTHON}" ]; then pip install ipython; fi

WORKDIR ${OPC_SRC}

COPY src ${OPC_SRC}/src
COPY README.md requirements.* setup.py ${OPC_SRC}

RUN pip install --no-cache-dir -r requirements.txt

USER opc
WORKDIR ${OPC_HOME}
ENTRYPOINT ["multi-opc"]

FROM centos:8.1.1911

# enable EPEL for all the newer crazy stuff
# like CMake 3
RUN     dnf install epel-release -y && dnf install -y 'dnf-command(config-manager)'
RUN     dnf config-manager --set-enabled PowerTools
# get the new packages from EPEL
# RUN        yum --disablerepo=* --enablerepo=epel check-update -y
RUN     dnf install -y \
        python3-pip

RUN     pip3 install pybombs


COPY ./docker_entrypoint.sh /

ENTRYPOINT ["/docker_entrypoint.sh"]

FROM centos:8.1.1911

# enable EPEL for all the newer crazy stuff
# like CMake 3
RUN     dnf install epel-release -y && dnf install -y 'dnf-command(config-manager)'
RUN     dnf config-manager --set-enabled PowerTools
# get the new packages from EPEL
# RUN        yum --disablerepo=* --enablerepo=epel check-update -y
RUN     dnf install -y \
        shadow-utils \
        cmake \
        gcc-c++ \
        libtool \
        alsa-lib-devel \
        boost-devel \
        codec2-devel \
        cppzmq-devel \
        desktop-file-utils \
        doxygen \
        fftw-devel \
        findutils \
        gmp-devel \
        graphviz \
        gsl-devel \
        gsm-devel \
        gtk3-devel \
        jack-audio-connection-kit-devel \
        log4cpp-devel \
        mpir-devel \
        orc-devel \
        portaudio-devel \
        python3-devel \
        python3-cairo \
        python3-click-plugins \
        python3-gobject \
        python3-numpy \
        python3-pyyaml \
        python3-lxml \
        python3-mako \
        python3-qt5-devel \
        python3-scipy \
        python3-six \
        python3-sphinx \
        python3-thrift \
        python3-mako \
        qwt-qt5-devel \
        SDL-devel \
        swig \
        thrift \
        uhd-devel \
        xdg-utils \
        xmlto \
        zeromq-devel \
        gtk3 

RUN     dnf install -y pinentry \
        git \
        make


RUN mkdir /packaging
WORKDIR /packaging

COPY ./docker_entrypoint.sh /

ENTRYPOINT ["/docker_entrypoint.sh"]

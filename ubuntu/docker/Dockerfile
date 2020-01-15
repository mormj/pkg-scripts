FROM ubuntu:18.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common && \
    DEBIAN_FRONTEND=noninteractive add-apt-repository -y ppa:mormj/gnuradio-master

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    libvolk2-dev \
    libthrift-dev \
    thrift-compiler \
    libcodec2-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends libuhd-dev \
    libvolk2-dev \
    thrift-compiler

RUN DEBIAN_FRONTEND=noninteractive apt-get install -qy \
    cmake \
    debhelper \
    dh-python \
    doxygen \
    graphviz \
    libasound2-dev \
    libboost-date-time-dev \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-regex-dev \
    libboost-system-dev \
    libboost-test-dev \
    libboost-thread-dev \
    libcppunit-dev \
    libfftw3-dev \
    libfontconfig1-dev \
    libgmp-dev \
    libgsl-dev \
    libgsm1-dev \
    libjack-jackd2-dev \
    liblog4cpp5-dev \
    liborc-0.4-dev \
    libportaudio2 \
    libpulse-dev \
    libqwt-qt5-dev \
    libsdl1.2-dev \
    libsndfile1-dev \
    libusb-1.0-0-dev \
    libxi-dev \
    libxrender-dev \
    libzmq3-dev \
    ninja-build \
    portaudio19-dev \
    python3-click \
    python3-click-plugins \
    python3-dev \
    python3-lxml \
    python3-mako \
    python3-numpy \
    python3-opengl \
    python3-pyqt5 \
    python3-scipy \
    python3-sphinx \
    python3-zmq \
    python3-pip \
    qt5-qmake \
    qtbase5-dev \
    qttools5-dev \
    swig \
    thrift-compiler \
    xmlto \
    git \
    ubuntu-dev-tools \
    bash-completion \
    python3-gi-cairo \
    python3-yaml \
    libgtk-3-dev \
    vim



ENTRYPOINT bash


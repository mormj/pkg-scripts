docker run --cpus 2 -it \
    -v /share/keys:/keys -v $(readlink -f ../../):/pkg-scripts/ \
    -v ~/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix/:/tmp/.X11-unix:rw \
    -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 \
    -v /share/tmp:/data \
    gr-centos8-pybombs "bash"

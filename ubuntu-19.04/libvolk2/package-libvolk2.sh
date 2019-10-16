# Copy the thrift package to the ppa

export DEBFULLNAME="Josh Morman"
export DEBEMAIL="mormjb@gmail.com"
export UBUMAIL="mormjb@gmail.com"
# export GPG_KEY=XXXXX...

backportpackage -d disco -u ppa:mormj/gnuradio-disco http://deb.debian.org/debian/pool/main/v/volk/volk_2.0.0-2.dsc -k $GPG_KEY -r

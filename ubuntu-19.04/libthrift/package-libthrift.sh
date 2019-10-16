# Copy the thrift package to the ppa

export DEBFULLNAME="Josh Morman"
export DEBEMAIL="mormjb@gmail.com"
export UBUMAIL="mormjb@gmail.com"
# export GPG_KEY=XXXXX...

backportpackage -d disco -u ppa:mormj/gnuradio-disco http://deb.debian.org/debian/pool/main/t/thrift/thrift_0.11.0-6.dsc -k $GPG_KEY -r

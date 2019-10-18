# Copy the thrift package to the ppa

export DEBFULLNAME="Josh Morman"
export DEBEMAIL="mormjb@gmail.com"
export UBUMAIL="mormjb@gmail.com"
# export GPG_KEY=XXXXX...

backportpackage -d bionic -u ppa:mormj/gnuradio-bionic http://deb.debian.org/debian/pool/main/u/uhd/uhd_3.14.1.1-1.dsc -k $GPG_KEY -r

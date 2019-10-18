# Copy the thrift package to the ppa

export DEBFULLNAME="Josh Morman"
export DEBEMAIL="mormjb@gmail.com"
export UBUMAIL="mormjb@gmail.com"
#export GPG_KEY=XXXXX...

backportpackage -d bionic -u ppa:mormj/gr http://deb.debian.org/debian/pool/main/c/codec2/codec2_0.8.1-2.dsc -k $GPG_KEY

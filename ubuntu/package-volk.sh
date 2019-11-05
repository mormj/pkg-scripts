# Packaging for Volk 2.0.0

DISTRIBUTION="disco"

mkdir build-volk

cd build-volk
wget http://deb.debian.org/debian/pool/main/v/volk/volk_2.0.0.orig.tar.xz
wget http://deb.debian.org/debian/pool/main/v/volk/volk_2.0.0-2.debian.tar.xz
tar xf volk_2.0.0.orig.tar.xz
tar xf volk_2.0.0-2.debian.tar.xz
mv debian volk-2.0.0
cd volk-2.0.0/debian
# manual step - update the changelog
dch -v 2.0.0-2 -b --distribution $DISTRIBUTION
debuild -S

cd ../../
dput -c ../dput.cf releases volk_2.0.0-2_source.changes

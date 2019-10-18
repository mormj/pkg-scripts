# Packaging for Volk 2.0.0

DISTRIBUTION="bionic"

mkdir build-volk

cd build-volk
wget http://deb.debian.org/debian/pool/main/v/volk/volk_2.0.0.orig.tar.xz
wget http://deb.debian.org/debian/pool/main/v/volk/volk_2.0.0-2.debian.tar.xz
tar xf volk_2.0.0.orig.tar.xz
tar xf volk_2.0.0-2.debian.tar.xz
mv debian volk-2.0.0
cd volk-2.0.0/debian
# manual step - update the changelog
dch -v 2.0.0-2~bionic -b --distribution bionic
debuild -S



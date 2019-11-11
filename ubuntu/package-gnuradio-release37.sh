# Automated Packaging for Ubuntu

NAME="Josh Morman"
EMAIL="<mormjb@gmail.com>"
DATESTR=$(date +"%a, %d %b %Y %T %z")
DISTRIBUTION="bionic"
PPA="gnuradio"

VERSION_MAJOR=3
VERSION_API=7
VERSION_ABI=13
VERSION_PATCH=5
REVISION=3

VERSION_STR="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH"
CHANGELOG="PPA build of $VERSION_STR"
echo $CHANGELOG
# Clone gnuradio repo
rm -rf build
mkdir build
cd build
git clone https://github.com/mormj/pkg-gnuradio.git

# Grab the tar.gz
FILENAME=gnuradio-$VERSION_STR.tar.gz
URL="https://www.gnuradio.org/releases/gnuradio/"
DOWNLOAD="$URL$FILENAME"
wget $DOWNLOAD
mv $FILENAME gnuradio_$VERSION_STR~$PPA~$DISTRIBUTION.orig.tar.gz
tar xf gnuradio_$VERSION_STR~$PPA~$DISTRIBUTION.orig.tar.gz
mv gnuradio-$VERSION_STR gnuradio
cd pkg-gnuradio
git checkout released37-$DISTRIBUTION

# Update changelog 
# gnuradio (3.9.0.0~368-6~bionic) bionic; urgency=medium
cd debian

# Update the changelog
# Increment the Debian Revision
cp changelog changelog.prev
echo -e "gnuradio ($VERSION_STR~$PPA~$DISTRIBUTION-$REVISION) $DISTRIBUTION; urgency=medium\n\n  * $PPA ppa Release of v$VERSION_STR for $DISTRIBUTION\n\n -- $NAME $EMAIL  $DATESTR\n\n$(cat changelog)" > changelog

# Start the build
cd ../../
cp -r pkg-gnuradio/debian gnuradio/
cd gnuradio/debian
#debuild -S -d
debuild 

exit

# dput the files to launchpad PPA
cd ../../
DEBFULLNAME="Josh Morman"
DEBEMAIL="mormjb@gmail.com"
UBUMAIL="mormjb@gmail.com"
#dput my-ppa gnuradio_$VERSION_STRING~$GITBRANCH_CLEAN~$GITREV~$DISTRIBUTION_source.changes 
dput -c ../dput.cf releases37 gnuradio_$VERSION_STR~$PPA~$DISTRIBUTION-"$REVISION"_source.changes

# check in the updated changelog
# TODO - update git branch to e.g. bionic-master, or bionic-maint-3.8
cd pkg-gnuradio
git add .
git commit -m " $PPA ppa Release of v$VERSION_STR"
#git push origin released37-$DISTRIBUTION

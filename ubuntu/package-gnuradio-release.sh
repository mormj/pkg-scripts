# Automated Packaging for Ubuntu

NAME="Josh Morman"
EMAIL="<mormjb@gmail.com>"
DATESTR=$(date +"%a, %d %b %Y %T %z")
DISTRIBUTION="bionic"

VERSION_MAJOR=3
VERSION_API=8
VERSION_ABI=0
VERSION_PATCH=0
REVISION=1

VERSION_STR="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH"
CHANGELOG="Unofficial build of $VERSION_STR"
echo $CHANGELOG
# Clone gnuradio repo
mkdir build
cd build
git clone https://github.com/mormj/pkg-gnuradio.git

# Grab the tar.gz
FILENAME=gnuradio-$VERSION_STR.tar.gz
URL="https://www.gnuradio.org/releases/gnuradio/"
DOWNLOAD="$URL$FILENAME"
wget $DOWNLOAD
mv $FILENAME gnuradio_$VERSION_STR~unofficial.orig.tar.gz
tar xf gnuradio_$VERSION_STR~unofficial.orig.tar.gz
mv gnuradio-$VERSION_STR gnuradio
cd pkg-gnuradio
git checkout released

# Update changelog 
# gnuradio (3.9.0.0~368-6~bionic) bionic; urgency=medium
cd debian

# Update the changelog
# Increment the Debian Revision
cp changelog changelog.prev
echo -e "gnuradio ($VERSION_STR~unofficial-$REVISION) $DISTRIBUTION; urgency=medium\n\n  * $GITBRANCH at $GIT_COMMIT\n\n -- $NAME $EMAIL  $DATESTR\n\n$(cat changelog)" > changelog

# Start the build
cd ../../
cp -r pkg-gnuradio/debian gnuradio/
cd gnuradio/debian
debuild -S

# dput the files to launchpad PPA
cd ../../
DEBFULLNAME="Josh Morman"
DEBEMAIL="mormjb@gmail.com"
UBUMAIL="mormjb@gmail.com"
#dput my-ppa gnuradio_$VERSION_STRING~$GITBRANCH_CLEAN~$GITREV~$DISTRIBUTION_source.changes 
dput -c ../dput.cf releases gnuradio_$VERSION_STR~unofficial-$REVISION_source.changes

# check in the updated changelog
# TODO - update git branch to e.g. bionic-master, or bionic-maint-3.8
#git add .
#git commit -m "build gnuradio from $"

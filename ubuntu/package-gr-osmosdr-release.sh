# Automated Packaging for Ubuntu

NAME="Josh Morman"
EMAIL="<mormjb@gmail.com>"
# NAME=$DEBFULLNAME
# EMAIL=$DEBEMAIL
DATESTR=$(date +"%a, %d %b %Y %T %z")
echo $DATESTR
# DISTRIBUTION=${1:-eoan}
# DISTRIBUTION="bionic"
# DISTRIBUTION="disco"
# DISTRIBUTION="eoan"
DISTRIBUTION="focal"
PPA="gnuradio"

VERSION_MAJOR=3
VERSION_API=8
VERSION_ABI=2
VERSION_PATCH=0
#RC="-rc1"
RC=""
REVISION=${2:-2}

VERSION_STR="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH$RC"
VERSION_STR_NO_RC="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH"
CHANGELOG="PPA build of $VERSION_STR"
echo $CHANGELOG
# Clone gnuradio repo
rm -rf build
mkdir build
cd build
git clone https://github.com/mormj/pkg-gr-osmosdr.git

# Grab the tar.gz
FILENAME=gnuradio-$VERSION_STR.tar.gz
# URL="https://www.gnuradio.org/releases/gnuradio/"
URL="https://github.com/gnuradio/gnuradio/releases/download/v$VERSION_STR/"
# DOWNLOAD="$URL$FILENAME"
DOWNLOAD=$URL$FILENAME
wget $DOWNLOAD
mv $FILENAME gnuradio_$VERSION_STR"-0"~$PPA~$DISTRIBUTION.orig.tar.gz
tar xf gnuradio_$VERSION_STR"-0"~$PPA~$DISTRIBUTION.orig.tar.gz
mv gnuradio-$VERSION_STR_NO_RC gnuradio
cd pkg-gnuradio
git checkout released-$DISTRIBUTION

# Update changelog 
# gnuradio (3.9.0.0~368-6~bionic) bionic; urgency=medium
cd debian

# Update the changelog
# Increment the Debian Revision
cp changelog changelog.prev
echo -e "gnuradio ($VERSION_STR-0~$PPA~$DISTRIBUTION-$REVISION) $DISTRIBUTION; urgency=medium\n\n  * $PPA ppa Release of v$VERSION_STR for $DISTRIBUTION\n\n -- $NAME $EMAIL  $DATESTR\n\n$(cat changelog)" > changelog

# Start the build
cd ../../
cp -r pkg-gnuradio/debian gnuradio/
cd gnuradio/debian
debuild -S -d
#debuild
# exit

# dput the files to launchpad PPA
cd ../../
DEBFULLNAME="Josh Morman"
DEBEMAIL="mormjb@gmail.com"
UBUMAIL="mormjb@gmail.com"
#dput my-ppa gnuradio_$VERSION_STRING~$GITBRANCH_CLEAN~$GITREV~$DISTRIBUTION_source.changes 
dput -c ../dput.cf releases gnuradio_$VERSION_STR"-0"~$PPA~$DISTRIBUTION-"$REVISION"_source.changes

# check in the updated changelog
# TODO - update git branch to e.g. bionic-master, or bionic-maint-3.8
cd pkg-gnuradio
git add .
git commit -m " $PPA ppa Release of v$VERSION_STR"
git push origin released-$DISTRIBUTION

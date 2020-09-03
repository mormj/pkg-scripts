# Automated Packaging for Ubuntu

NAME="Josh Morman"
EMAIL="<mormjb@gmail.com>"
DATESTR=$(date +"%a, %d %b %Y %T %z")
echo $DATESTR
# DISTRIBUTION=${1:-eoan}
# DISTRIBUTION="bionic"
# DISTRIBUTION="disco"
# DISTRIBUTION="eoan"
DISTRIBUTION="focal"
PPA="gnuradio"

# OOT_NAME="gr-fcdproplus"
# PKG_GIT="https://salsa.debian.org/debian-hamradio-team/pkg-gr-fcdproplus"
# SRC_GIT="https://github.com/dl1ksv/gr-fcdproplus"
# GITBRANCH="master"
# REVISION="4+b1"
# SUFFIX="4"

# OOT_NAME="sdrangelove"
# PKG_GIT="https://salsa.debian.org/debian-hamradio-team/pkg-sdrangelove"
# SRC_GIT="git://git.osmocom.org/sdrangelove.git"
# GITBRANCH="master"
# REVISION="4+b1"
# SUFFIX="4"

# OOT_NAME="gr-osmosdr"
# PKG_GIT="https://salsa.debian.org/bottoms/pkg-gr-osmosdr"
# SRC_GIT="https://github.com/osmocom/gr-osmosdr"
# GITBRANCH="master"
# REVISION="0"

OOT_NAME="gr-limesdr"
PKG_GIT="https://github.com/mormj/pkg-gr-limesdr"
SRC_GIT="https://github.com/myriadrf/gr-limesdr"
GITBRANCH="gr-3.8"
REVISION="3"
SUFFIX="3"

# OOT_NAME="gr-iqbal"
# PKG_GIT="https://github.com/mormj/pkg-gr-iqbal"
# SRC_GIT="https://github.com/osmocom/gr-iqbal"
# GITBRANCH="master"
# REVISION="4+b4"
# SUFFIX="7"

# OOT_NAME="gr-fosphor"
# PKG_GIT="https://salsa.debian.org/bottoms/pkg-gr-fosphor"
# SRC_GIT="https://github.com/osmocom/gr-fosphor"
# GITBRANCH="master"
# REVISION="4+b2"
# SUFFIX="5"


# https://salsa.debian.org/bottoms/pkg-gr-iqbal
# https://salsa.debian.org/bottoms/pkg-gr-fosphor
# https://salsa.debian.org/bottoms/pkg-gqrx-sdr

GITBRANCH_CLEAN=${GITBRANCH/-/}
# GNU Radio Version that we are compiling against - TBD how to use this
VERSION_MAJOR=3
VERSION_API=8
VERSION_ABI=2
VERSION_PATCH=0


# Clone gnuradio repo
rm -rf build
mkdir build
cd build
git clone $PKG_GIT
git clone $SRC_GIT

cd $OOT_NAME
git checkout $GITBRANCH
VERSION_MAJOR="$(cat CMakeLists.txt | grep -i "SET(VERSION_MAJOR" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_API="$(cat CMakeLists.txt | grep -i  "SET(VERSION_API" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_ABI="$(cat CMakeLists.txt | grep -i "SET(VERSION_ABI" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_PATCH="$(cat CMakeLists.txt | grep -i "SET(VERSION_PATCH" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_STR="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH$RC"
echo $VERSION_STR
cd ..

VERSION_STR_NO_RC="$VERSION_MAJOR.$VERSION_API.$VERSION_ABI.$VERSION_PATCH"
CHANGELOG="PPA build of $OOT_NAME $VERSION_STR"
echo $CHANGELOG

cd $OOT_NAME
git checkout $GITBRANCH
git submodule init
git submodule update
GITREV="$(git rev-list --count HEAD)"

echo "Creating build for GNU Radio "$VERSION_STR

GIT_COMMIT="$(git log --pretty=oneline | head -n 1)"
echo $GIT_COMMIT

# Tar.gz it
rm -rf .git
cd ..

echo "@#$^@#%@#$%@#$%@#$%"
echo $OOT_NAME
echo "${OOT_NAME}"_"${VERSION_STR}-${REVISION}"~"${PPA}"~"${DISTRIBUTION}".orig.tar
tar -cf "${OOT_NAME}"_"${VERSION_STR}-${REVISION}"~"${PPA}"~"${DISTRIBUTION}".orig.tar $OOT_NAME
gzip "${OOT_NAME}"_"${VERSION_STR}-${REVISION}"~"${PPA}"~"${DISTRIBUTION}".orig.tar
cp "${OOT_NAME}"_"${VERSION_STR}-${REVISION}"~"${PPA}"~"${DISTRIBUTION}".orig.tar.gz "${OOT_NAME}"_"${VERSION_STR}".orig.tar.gz 
cd pkg-$OOT_NAME

# Update changelog 
# gnuradio (3.9.0.0~368-6~bionic) bionic; urgency=medium
cd debian

# Update the changelog
# Increment the Debian Revision
cp changelog changelog.prev
echo -e "$OOT_NAME ($VERSION_STR-$REVISION~$PPA~$DISTRIBUTION-$SUFFIX) $DISTRIBUTION; urgency=medium\n\n  * $PPA ppa Release of v$VERSION_STR for $DISTRIBUTION\n\n -- $NAME $EMAIL  $DATESTR\n\n$(cat changelog)" > changelog

# Start the build
cd ../../
cp -r pkg-$OOT_NAME/debian $OOT_NAME/
cd $OOT_NAME/debian
debuild -S -d -rfakeroot
#debuild
# exit

# dput the files to launchpad PPA
cd ../../
DEBFULLNAME="Josh Morman"
DEBEMAIL="mormjb@gmail.com"
UBUMAIL="mormjb@gmail.com"
#dput my-ppa gnuradio_$VERSION_STRING~$GITBRANCH_CLEAN~$GITREV~$DISTRIBUTION_source.changes 
dput -c ../dput.cf oot "${OOT_NAME}_${VERSION_STR}"-"${REVISION}~${PPA}~${DISTRIBUTION}-${SUFFIX}"_source.changes

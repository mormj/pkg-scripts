# Automated Packaging for Ubuntu

NAME="Josh Morman"
EMAIL="<mormjb@gmail.com>"
DATESTR=$(date +"%a, %d %b %Y %T %z")
DISTRIBUTION="disco"
DEBREV="368-7"
GITBRANCH=master

if true; then
# Clone gnuradio repo
mkdir build
cd build
git clone https://github.com/gnuradio/gnuradio.git 
git clone https://github.com/mormj/pkg-gnuradio.git
else
cd build
fi

cd gnuradio

# Scrape the version number from CMakeLists.txt
VERSION_MAJOR="$(cat CMakeLists.txt | grep "SET(VERSION_MAJOR" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_API="$(cat CMakeLists.txt | grep "SET(VERSION_API" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_ABI="$(cat CMakeLists.txt | grep "SET(VERSION_ABI" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_PATCH="$(cat CMakeLists.txt | grep "SET(VERSION_PATCH" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"

# Remove '-' from the patch
VERSION_PATCH=${VERSION_PATCH/-/}

VERSION_STRING=$VERSION_MAJOR"."$VERSION_API"."$VERSION_ABI"."$VERSION_PATCH
echo "Creating build for GNU Radio "$VERSION_STRING

GIT_COMMIT="$(git log --pretty=oneline | head -n 1)"
echo $GIT_COMMIT

cd ..

# Tar.gz it
tar -cf gnuradio_$VERSION_STRING~$DEBREV~$DISTRIBUTION.orig.tar gnuradio
gzip gnuradio_$VERSION_STRING~$DEBREV~$DISTRIBUTION.orig.tar

cd pkg-gnuradio
git checkout $DISTRIBUTION

# Update changelog 
# gnuradio (3.9.0.0~368-6~bionic) bionic; urgency=medium
cd debian

# If latest commit is same as what is checked into the changelog
LAST_GIT_COMMIT="$(cat changelog | head -n 3 | tail -n 1 | tr -s ' ' | cut -d " " -f3)"
CURR_GIT_COMMIT="$(echo $GIT_COMMIT | cut -d " " -f1)"

echo "Previous Git Commit string $LAST_GIT_COMMIT"
echo "Current Git Commit string $CURR_GIT_COMMIT"

if [$LAST_GIT_COMMIT == $CURR_GIT_COMMIT]; then
echo "  No change in git tags, no need to make a build"
exit 1
fi

# Update the changelog
# Increment the Debian Revision
cp changelog changelog.prev
echo -e "gnuradio ($VERSION_STRING~$DEBREV~$DISTRIBUTION) $DISTRIBUTION; urgency=medium\n\n  * $GITBRANCH at $GIT_COMMIT\n\n -- $NAME $EMAIL  $DATESTR\n\n$(cat changelog)" > changelog

# Start the build
cd ../../
cp -r pkg-gnuradio/debian gnuradio/
cd gnuradio/debian
debuild -us -uc

# dput the files to launchpad PPA

# check in the updated changelog


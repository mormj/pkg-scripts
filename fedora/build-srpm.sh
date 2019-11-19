release="1"

if true; then
rm -rf build
mkdir build
cd build

cp ~/git/pkg-gnuradio/fedora/gnuradio.spec ./

rm -rf rpmbuild
mkdir -p rpmbuild
mkdir -p rpmbuild/BUILD
mkdir -p rpmbuild/BUILDROOT
mkdir -p rpmbuild/RPMS
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SRPMS

DATESTR=$(date +"%a, %d %b %Y %T %z")
DISTRIBUTION="fedora"
GITBRANCH=master
GITBRANCH_CLEAN=${GITBRANCH/-/}

# Clone gnuradio repo
git clone https://github.com/gnuradio/gnuradio.git --recurse-submodules
#git clone https://github.com/mormj/pkg-gnuradio.git

cd gnuradio
git checkout $GITBRANCH
GITREV="$(git rev-list --count HEAD)"

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

# Tar.gz it

cd ..
cp -r gnuradio "gnuradio-$VERSION_STRING"
cd "gnuradio-$VERSION_STRING"
rm -rf .git
cd ..
tar cfJ rpmbuild/SOURCES/gnuradio_$VERSION_STRING~$GITBRANCH_CLEAN~$GITREV~$DISTRIBUTION.tar.xz gnuradio-$VERSION_STRING

else
DISTRIBUTION="fedora"
GITBRANCH=master
GITBRANCH_CLEAN=${GITBRANCH/-/}

cd build
cp ~/git/pkg-gnuradio/fedora/gnuradio.spec ./
cd gnuradio
git checkout $GITBRANCH
GITREV="$(git rev-list --count HEAD)"

# Scrape the version number from CMakeLists.txt
VERSION_MAJOR="$(cat CMakeLists.txt | grep "SET(VERSION_MAJOR" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_API="$(cat CMakeLists.txt | grep "SET(VERSION_API" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_ABI="$(cat CMakeLists.txt | grep "SET(VERSION_ABI" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"
VERSION_PATCH="$(cat CMakeLists.txt | grep "SET(VERSION_PATCH" | tr -s ' ' | cut -d' ' -f2 | cut -d')' -f1)"

# Remove '-' from the patch
VERSION_PATCH=${VERSION_PATCH/-/}

VERSION_STRING=$VERSION_MAJOR"."$VERSION_API"."$VERSION_ABI"."$VERSION_PATCH
echo "Creating build for GNU Radio "$VERSION_STRING

cd ..

fi

sed -i 's/\%{VERSION}/'$VERSION_STRING'/g' gnuradio.spec
sed -i 's/\%{RELEASE}/'$release'/g' gnuradio.spec

SOURCE="gnuradio_$VERSION_STRING~$GITBRANCH~$GITREV~fedora.tar.xz"
sed -i 's/\%{SOURCE}/'$SOURCE'/g' gnuradio.spec

rpmbuild \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  -bs gnuradio.spec
	  #--noclean -ba gnuradio.spec
#	  -bs gnuradio.spec
# 	  --noclean -ba gnuradio.spec
#
#

#	  
#	  -bs gnuradio.spec
	  
#	  	  --noclean \

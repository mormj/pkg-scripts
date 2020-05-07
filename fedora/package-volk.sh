release="1"

rm -rf build
mkdir build
cp volk.spec build/
cd build

# cp ~/git/pkg-gnuradio/fedora/gnuradio.spec ./

rm -rf rpmbuild
mkdir -p rpmbuild
mkdir -p rpmbuild/BUILD
mkdir -p rpmbuild/BUILDROOT
mkdir -p rpmbuild/RPMS
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SRPMS

spectool -g volk.spec -C rpmbuild/SOURCES/

rpmbuild \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  -bs volk.spec
	#   --noclean -ba volk.spec
#	  -bs gnuradio.spec
# 	  --noclean -ba gnuradio.spec
#
#

#	  
#	  -bs gnuradio.spec
	  
#	  	  --noclean \
#copr-cli build gnuradio-master build/rpmbuild/SRPMS/gnuradio-3.9.0.0git-1.fc31.src.rpm 

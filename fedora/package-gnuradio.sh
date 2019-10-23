version="2.0.0"
release="1"
name="volk"
full_name="$name-$version"
download_url="https://github.com/gnuradio/$name/archive/v$version.tar.gz"

rm -rf rpmbuild
mkdir -p rpmbuild
mkdir -p rpmbuild/BUILD
mkdir -p rpmbuild/BUILDROOT
mkdir -p rpmbuild/RPMS
mkdir -p rpmbuild/SOURCES
mkdir -p rpmbuild/SRPMS

curl -L -o rpmbuild/SOURCES/$full_name.tar.gz $download_url; 

# Edit the spec file directly
cp volk-template.spec volk.spec
sed -i 's/\%{VERSION}/'$version'/g' volk.spec
sed -i 's/\%{RELEASE}/'$release'/g' volk.spec

rpmbuild \
	  --define "_topdir %(pwd)" \
	  --define "_builddir %{_topdir}/rpmbuild/BUILD" \
	  --define "_buildrootdir %{_topdir}/rpmbuild/BUILDROOT" \
	  --define "_rpmdir %{_topdir}/rpmbuild/RPMS" \
	  --define "_srcrpmdir %{_topdir}/rpmbuild/SRPMS" \
	  --define "_specdir %{_topdir}" \
	  --define "_sourcedir %{_topdir}/rpmbuild/SOURCES" \
	  --noclean \
	  -bs volk.spec



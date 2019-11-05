# NEON support is by default enabled on aarch64 and disabled on other ARMs (it can be overridden)
%ifarch aarch64
%bcond_without neon
%else
%bcond_with neon
%endif

%{!?python3_sitearch: %global python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%ifarch %{arm}
%if %{with neon}
%global my_optflags %(echo -n "%{optflags}" | sed 's/-mfpu=[^ \\t]\\+//g'; echo " -mfpu=neon")
%{expand: %global optflags %{my_optflags}}
%global mfpu_neon -Dhave_mfpu_neon=1
%else
%global mfpu_neon -Dhave_mfpu_neon=0
%endif
%endif

# For versions not yet on ftp, pull from git
#%%global git_commit 441a3767e05d15e62c519ea66b848b5adb0f4b3a

#%%global alphatag rc1

Name:		gnuradio
Version:	%{VERSION}
Release:	%{RELEASE}%{?alphatag:.%{alphatag}}%{?dist}
Summary:	Software defined radio framework

License:	GPLv3
URL:		http://www.gnuradio.org
#Source0:	ftp://ftp.gnu.org/gnu/gnuradio/gnuradio-%%{version}.tar.gz
#Source0:	http://gnuradio.org/redmine/attachments/download/%%{attachment_id}/gnuradio-%%{version}.tar.gz
#sSource0:	http://gnuradio.org/releases/gnuradio/gnuradio-%{version}%{?alphatag}.tar.xz
#Source0:	http://gnuradio.org/releases/gnuradio/gnuradio-%%{version}.tar.gz
Source:     %{SOURCE} 
# git clone git://gnuradio.org/gnuradio
# cd gnuradio
# git archive --format=tar --prefix=%%{name}-%%{version}/ %%{git_commit} | \
# gzip > ../%%{name}-%%{version}.tar.gz

Requires(pre):	shadow-utils
BuildRequires:	cmake, fftw-devel, cppunit-devel, xmlto
BuildRequires:	graphviz, boost-devel, python3-devel, swig, doxygen
BuildRequires:	libusbx-devel, SDL-devel, guile-devel
BuildRequires:	portaudio-devel, libtool, gsm-devel
# Gnuradio deprecated gr-comedi
# http://gnuradio.org/redmine/issues/show/395
# BuildRequires: comedilib-devel
BuildRequires:	gsl-devel, numpy, PyQt5-devel, python3-pyqtgraph
BuildRequires:	python3-lxml, pygtk2-devel, orc-devel
BuildRequires:	desktop-file-utils, python3-mako, python3-six
BuildRequires:	uhd-devel, python3, cppzmq-devel, zeromq-devel, thrift
BuildRequires:	python3-sphinx, codec2-devel, findutils, python3-matplotlib
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:  log4cpp-devel, mpir-devel
#BuildRequires:	python3-thrift
%if ! 0%{?rhel:1}
BuildRequires:	qwt-devel
%endif
Requires:	numpy, scipy, portaudio, python3-lxml
Requires:	pygtk2, PyQt5, zeromq, log4cpp-devel
#Requires:	python3-thrift
%if ! 0%{?rhel:1}
Requires:	python3-pyopengl
%endif
Obsoletes:	usrp < 3.3.0-1
Obsoletes:	grc < 0.80-1
# rhbz#1143914, patch approved by upstream to be used as distro specific
# patch, upstream report: http://gnuradio.org/redmine/issues/728
#Patch0:	gnuradio-3.7.13.3-size_t.patch
#Patch0: 	

%description
GNU Radio is a collection of software that when combined with minimal
hardware, allows the construction of radios where the actual waveforms
transmitted and received are defined by software. What this means is
that it turns the digital modulation schemes used in today's high
performance wireless devices into software problems.

%package devel
Summary:	GNU Radio
Requires:	%{name} = %{version}-%{release}
Requires:	cmake, boost-devel
Obsoletes:	usrp-devel <  3.3.0-1

%description devel
GNU Radio Headers

%package doc
Summary:	GNU Radio
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
GNU Radio Documentation

%package examples
Summary:	GNU Radio
Requires:	%{name} = %{version}-%{release}

%description examples
GNU Radio examples

%prep
%setup -q -n %{name}-%{version}%{?alphatag}
#%patch0 -p1 -b .size_t

# Use cmake's FindGSL.cmake instead
#rm cmake/Modules/FindGSL.cmake

#force regeneration of cached moc output files
find . -name "*_moc.cc" -exec rm {} \;

%build
mkdir build
cd build
%cmake \
-DSYSCONFDIR=%{_sysconfdir} \
-DGR_PKG_DOC_DIR=%{_docdir}/%{name} \
-DENABLE_DOXYGEN=FALSE \
%{?mfpu_neon} \
..

make %{?_smp_mflags} CFLAGS="%{optflags} -fno-strict-aliasing" CXXFLAGS="%{optflags} -fno-strict-aliasing"

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR=%{buildroot}
popd

# remove atsc example (bytecompilation problem)
# the examples shouldn't be probably bytecompiled,
# but selective bytecompilation would take a lot of time,
# thus letting it as is
#rm -rf %{buildroot}%{_datadir}/%{name}/examples/atsc

## install desktop file, icons, and MIME configuration to right locations
#tree %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
#desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
#  %{buildroot}%{_datadir}/%{name}/grc/freedesktop/gnuradio-grc.desktop
#mkdir -p %{buildroot}%{_datadir}/mime/packages
#mv %{buildroot}%{_datadir}/%{name}/grc/freedesktop/gnuradio-grc.xml %{buildroot}%{_datadir}/mime/packages
#for x in 32 48 64 128 256
#do
#  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${x}x${x}/apps
#  mv %{buildroot}%{_datadir}/%{name}/grc/freedesktop/grc-icon-${x}.png %{buildroot}%{_datadir}/icons/hicolor/${x}x${x}/apps/gnuradio-grc.png
#done
#rm -f %{buildroot}%{_datadir}/%{name}/grc/freedesktop/*
#rmdir %{buildroot}%{_datadir}/%{name}/grc/freedesktop

# fix hashbangs
pushd %{buildroot}%{_bindir}
sed -i '1 s/^\(#!\/usr\/bin\/\)\(env\|python\).*$/\1python3/' gr-ctrlport-monitor gr-perf-monitorx
popd

%ldconfig_scriptlets

%files
%license COPYING
%{python3_sitearch}/*
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libexecdir}/*
%{_datadir}/gnuradio
%{_datadir}/applications/gnuradio-grc.desktop
%{_datadir}/mime/packages/gnuradio-grc.xml
%{_datadir}/icons/hicolor/*/apps/gnuradio-grc.png
%config(noreplace) %{_sysconfdir}/gnuradio
%exclude %{_datadir}/gnuradio/examples
%exclude %{_docdir}/%{name}/html
%exclude %{_docdir}/%{name}/xml
%doc %{_docdir}/%{name}

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/volk
%{_libdir}/cmake/gnuradio

%files doc
%doc %{_docdir}/%{name}/html
%doc %{_docdir}/%{name}/xml

%files examples
%{_datadir}/gnuradio/examples

%changelog
* Thu Jan 31 2019 Josh Morman <mormjb@gmail.com> - 3.9.0.0git-1
- Rebuilt from GNU Radio master

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.13.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 3.7.13.4-4
- Rebuilt for Boost 1.69

* Fri Aug 10 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.4-3
- Dropped patented content
  Resolves: rhbz#1608973
- Enabled ZeroMQ, sphinx, comedilib, jack, and log4cpp
  Resolves: rhbz#1610513
- Temporaly disabled doxygen (the doc subpackage is mostly useless now),
  because due to various bugs in different packages the documentation builds
  differently on different architectures
- Fixed python hashbangs
- Unlimited number of make processes

* Sun Jul 22 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.4-2
- Rebuilt for new uhd

* Tue Jul 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.4-1
- New version
  Resolves: rhbz#1601288
  Resolves: rhbz#1601263

* Mon Jul 16 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-7
- Fixed python2 macros

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.13.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-5
- Rebuild to fix provides

* Wed Jul  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-4
- Fixed python requirements

* Wed Jun 27 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-3
- Added all upstream cmake modules

* Mon Jun 18 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-2
- Added some missing cmake modules

* Fri Jun 15 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.13.3-1
- New version
  Resolves: rhbz#1591524
- Dropped gcc-7-compile fix patch (not needed)
- De-fuzzified size_t patch

* Thu Feb 22 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.11-10
- Rebuilt for new python-cheetah

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb  2 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.11-8
- Rebuilt for new boost

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.7.11-7
- Remove obsolete scriptlets

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 3.7.11-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 3.7.11-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.11-3
- Rebuilt for new gsl

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 3.7.11-2
- Rebuilt for Boost 1.64

* Wed May 24 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.11-1
- New version

* Tue Feb 07 2017 Kalev Lember <klember@redhat.com> - 3.7.10.1-5
- Rebuilt for Boost 1.63

* Tue Nov 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.10.1-4
- Rebuilt for new uhd

* Thu Sep 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.10.1-3
- Uncoditionally enabled NEON support on aarch64

* Fri Sep 16 2016 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.10.1-2
- NEON is compulary part of aarch64 so enable unconditionally on that arch

* Wed Aug 31 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.10.1-1
- New version
  Resolves: rhbz#1370728

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.10-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul  4 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.10-1
- New version
  Resolves: rhbz#1352483
- Dropped stdc11-fix and cmake35 patches (both upstreamed)
- Defuzzified size_t patch

* Tue May 10 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.9.1-4
- Rebuilt for new uhd

* Mon Mar  7 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.9.1-3
- Rebuilt for new gsl

* Tue Feb 23 2016 Orion Poplawski <orion@cora.nwra.com> - 3.7.9.1-2
- Rebuild for gsl 2.1
- Add patch for cmake 3.5 (bug #1311358)

* Wed Feb 10 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.9.1-1
- New version
  Resolves: rhbz#1306066

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 3.7.9-2
- Rebuilt for Boost 1.60

* Mon Jan  4 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.9-1
- New version
  Resolves: rhbz#1294379

* Tue Dec 15 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.9-0.1.rc1
- New version
  Resolves: rhbz#1291659
- Dropped dos2unix and conversion from CR + LF to LF (not needed)

* Thu Nov  5 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.8.1-1
- New version
  Resolves: rhbz#1276888

* Thu Oct  1 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.8-3
- Fixed icon and desktop file locations
  Resolves: rhbz#1266700

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.7.8-2
- Rebuilt for Boost 1.59

* Wed Aug 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.8-1
- New version
  Resolves: rhbz#1251650

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Mon Jul 27 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.8-0.1.rc1
- New version
  Resolves: rhbz#1246803
- Updated size_t patch
- Dropped docdir-override (not needed)

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.7.7.1-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.7.1-1
- New version
  Resolves: rhbz#1220588
- Rebased size_t patch
- Dropped volk-memalign-fix patch (not needed)
- Dropped wxpython3-gtk3 patch (upstreamed)
- Set DOCDIR to match Fedora documentation location (by docdir-override patch)

* Sun May 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.7.6.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.6.1-3
- Enabled uhd on ppc64 on RHEL-7
- Built with -j2 to speed-up the build process a bit

* Wed Mar 11 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.6.1-2
- Enabled optional building with NEON support on aarch64
- Built with -j1 to prevent internal compiler errors due to excessive
  use of resources

* Thu Feb 19 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.6.1-1
- New version
  Resolves: rhbz#1193588
- De-fuzzified size_t patch

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 3.7.5.1-5
- Bump for rebuild.

* Thu Jan 29 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5.1-4
- Added fix for wxPython3 (by wxpython3-gtk3 patch). Patch
  provided by Scott Talbert

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.7.5.1-3
- Rebuild for boost 1.57.0

* Mon Jan 26 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5.1-2
- Workaround for volk memalign (by volk-memalign-fix patch)
  Resolves: rhbz#1185710
- Rebuilt for current uhd
  Resolves: rhbz#1185508

* Tue Oct 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5.1-1
- New versio
  Resolves: rhbz#1155252

* Tue Oct  7 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5-3
- Fixed swig bug regarding size_t (by size_t patch)
  This fixes building on s390
  Resolves: rhbz#1143914

* Wed Sep 17 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5-2
- Added PyOpenGL requirement
  Resolves: rhbz#1049770

* Mon Sep  1 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.5-1
- New version
  Resolves: rhbz#1135814

* Mon Aug 18 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.4-6
- Removed explicit PyQwt requirement on RHEL-7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.4-4
- Fixed building on RHEL-7

* Fri Aug  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.4-3
- Enabled UHD on RHEL-7 non ppc64

* Fri Aug  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.4-2
- Added workaround to build on RHEL-7

* Wed Jul 16 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.4-1
- New version
  Resolves: rhbz#1120106
- Dropped system-gsm patch (not needed)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 3.7.3-3
- rebuild for boost 1.55.0

* Sun Mar 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.7.3-2
- Use system gsm instead of bundled one

* Tue Mar 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.3-1
- New version
  Resolves: rhbz#1074899
- Dropped qwt61 patch (not needed)

* Tue Feb 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.2.1-4
- Rebuilt due to new uhd

* Mon Jan  6 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.2.1-3
- Enabled use of qwt61 (by qwt61 patch)
  Resolves: rhbz#1045935
- Added sphinx to buildrequires
  Related: rhbz#1045935
- Fixed whitespaces in description

* Fri Jan  3 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.2.1-2
- Added boost-devel as requirement for gnuradio-devel
  Resolves: rhbz#1002148

* Mon Dec  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.2.1-1
- New version
  Resolves: rhbz#1036554

* Mon Nov 18 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.2-1
- New version
  Resolves: rhbz#1030865
- Dropped uhd-fft-err, cmake-libdir patches (all upstreamed)

* Tue Sep 17 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.1-5
- Fixed defaults to use libdir for cmake modules (by cmake-libdir patch)
- Defuzzified uhd-fft-err patch

* Tue Sep 17 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.1-4
- Moved cmake modules to libdir/cmake

* Wed Sep  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.1-3
- Fixed FindGnuradio.cmake (by findgnuradio-cmake-fix patch)

* Mon Sep  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.1-2
- Do not install bundled cmake modules

* Mon Sep  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.1-1
- New version
  Resolves: rhbz#1003319
- Dropped cmake-modules-fix, bigendian, build-fix patches (upstreamed)
- Fixed uhd_fft error handling
  Resolves: rhbz#1003075

* Tue Aug  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.0-0.5.rc0
- Used unversioned doc directory
  Resolves: rhbz#993794

* Tue Jul 30 2013 Dennis Gilmore <dennis@ausil.us> - 3.7.0-0.4.rc0
- rebuild against 1.54.0 again

* Mon Jul 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.0-0.3.rc0
- Symlinked FindGnuradio.cmake

* Sun Jul 28 2013 Petr Machata <pmachata@redhat.com> - 3.7.0-0.2.rc0
- Rebuild for boost 1.54.0

* Mon Jun 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7.0-0.1.rc0
- New version
  Resolves: rhbz#976982
- Defuzzified cmake-modules-fix patch

* Wed Jun 12 2013 Dan Horák <dan[at]danny.cz> - 3.6.5-2
- fix build on big endian arches

* Tue Jun  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.5-1
- New version
  Resolves: rhbz#967804
- Make cmake modules installation directory configurable
  (by cmake-modules-fix patch)
- Tried to switch back to parallel build (hopefully the koji builder
  machines have now enough resources)

* Wed Mar 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.4.1-1
- New version
  Resolves: rhbz#923699

* Thu Feb 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.4-1
- New version
  Resolves: rhbz#916530

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.6.3-0.4.rc0
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 3.6.3-0.3.rc0
- Rebuild for Boost-1.53.0

* Fri Jan 11 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.3-0.2.rc0
- Fixed unowned directories
  Resolves: rhbz#894200

* Wed Jan  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.3-0.1.rc0
- New version
  Resolves: rhbz#890393
- Fixed bogus date in changelog

* Thu Nov 15 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.2-4
- Added PyQwt requirement
  Resolves: rhbz#876830

* Wed Oct 31 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.2-3
- Forced gr-core build

* Tue Oct 30 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.2-2
- Fixed libusb requirements
- Enabled gr-fcd
  Resolves: rhbz#871513

* Thu Oct 25 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.2-1
- New version
  Resolves: rhbz#869840
- Dropped neon patch (upstreamed)

* Fri Oct 19 2012 Rex Dieter <rdieter@fedoraproject.org> 3.6.1-8
- rebuild (qwt)

* Mon Sep 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-7
- Fixed doc subpackage to be noarch

* Wed Aug 29 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-6
- Added conditional for ARM NEON build (%%bcond_with neon)

* Fri Aug 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-5
- Rebuilt for new boost

* Tue Jul 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-4
- On non ARM expand disable_mfpu_neon macro to empty string

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-2
- Disabled NEON optimisations (neon patch, sent upstream)
  Resolves: rhbz#837028
- Removed sdcc build requires (not needed)

* Tue Jun 12 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.1-1
- New version
  Resolves: rhbz#831187
  Dropped pygtk2-no-x-detect patch (upstreamed)

* Mon Apr 23 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6.0-1
- New version
  Resolves: rhbz#815070
- Dropped ARM patch (not used in new buildsystem)
- Fixed pygtk detection (pygtk2-no-x-detect patch)

* Wed Apr 18 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.3.1-1
- New version
  Resolves: rhbz#813725

* Wed Apr 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.3-2
- Fix building on ARM

* Tue Apr 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.3-1
- New version
  Resolves: rhbz#810683

* Tue Mar 27 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.2.1-2
- Rebuilt with new uhd

* Fri Mar 16 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.2.1-1
- New version
  Resolves: rhbz#804032

* Thu Mar 15 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.2-1
- New version
  Resolves: rhbz#802950
- Dropped compile-fix patch (upstreamed)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for c++ ABI breakage

* Tue Jan 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.1-2
- Added explicit requires on PyQt4
  Resolves: rhbz#781494

* Fri Jan 13 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.1-1
- New version
  Resolves: rhbz#781355
- Fixed compilation with gcc-4.7.0 (compile-fix patch)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.0-2
- Fixed double packaging of doc
  Resolves: rhbz#769069
- Fixed rpmlint warnings

* Tue Dec 13 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.0-1
- New version
- Used macros instead of variables in spec
- Dropped sdcc hack, was needed by obsoleted libusrp

* Sun Dec  4 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.0-0.2.rc0
- Added python-cheetah dependency
  Resolves: rhbz#759834

* Fri Dec 02 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5.0-0.1.rc0
- New pre-release version
- Followed upstream and dropped support for usrp, use uhd instead
- Dropped sdcc3 and libusb-detect-fix patches
- Dropped 10-usrp.rules and usrp group creation, now handled by uhd

* Sun Nov 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.2-2
- Rebuilt for new boost

* Thu Oct 27 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.2-1
- New version
- Dropped retval patch

* Fri Oct 21 2011 Dan Horák <dan[at]danny.cz> - 3.4.0-5
- add missing return value in generated code
- add BR: orc-devel - needed for secondary arches in volk

* Thu Oct 20 2011 Dan Horák <dan[at]danny.cz> - 3.4.0-4
- explicitly set boost libdir to workaround build failures on non-x86 64-bit arches

* Thu Jul 21 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.0-3
- Enabled volk
- Rebuilt for new boost

* Sun Jul 03 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.0-2
- Rebuilt with -j1, otherwise the build process may fail on machines with low RAM
- Define changed to global

* Mon Jun 27 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.0-1
- New version
- Updated 10-usrp.rules
  Resolves: rhbz#597023
- Merged usrp to gnuradio, fixes some packaging bugs
  Resolves: rhbz#516352
  Resolves: rhbz#619195
- Rebuilt with included grc, obsoleted grc package
  Resolves: rhbz#592486
- Removed unneeded patches (libtool, configure, gcc45, ptrdifft-std)
- Fixed compilation with sdcc3 (sdcc3 patch)
- Fixed detection of libusb (libusb-detect-fix patch)
- Compiled with -fno-strict-aliasing

* Thu Apr 07 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.2.2-13
- Rebuild for new boost

* Tue Mar 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.2.2-12
- Rebuild for new boost

* Tue Feb 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.2.2-11
- Fix compilation with ptrdifft-std patch
- Rebuild for new boost

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-9
- rebuild for new boost

* Tue Sep 07 2010 Dan Horák <dan[at]danny.cz> - 3.2.2-8
- Add sparc64 and s390x to 64-bit platforms

* Sun Aug 01 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 3.2.2-7
- Fix gcc-4.5 build errors

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.2-5
- re-export PATH for %%install

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.2-4
- don't BuildRequires: comedilib-devel, code doesn't use it

* Tue Feb 09 2010 Caolán McNamara <caolanm@redhat.com> - 3.2.2-3
- Resolves: rhbz#539069 FTBFS

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 3.2.2-2
- Rebuild for Boost soname bump

* Wed Jul 29 2009 Marek Mahut <mmahut@fedoraproject.org> - 3.2.2-1
- Upstream release 3.2.2
- Dropped patch gnuradio-3.2-gcc44.patch

* Sat Jul 25 2009 Marek Mahut <mmahut@fedoraproject.org> - 3.2-1
- Upstream release 3.2

* Wed Mar  4 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.1.3-5
- Fix build with GCC 4.4

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 31 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.3-3
- Adding udev rule for USRP device
- Adding usrp system group

* Fri Dec 19 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.3-2
- Upstream release 3.1.3
- Comedi support
- RHBZ#473928 Unowned directories  

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.1.2-3
- Rebuild for Python 2.6

* Tue Jun 10 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.2-2
- Moving usrp header files to usrp-devel (reported by Philip Balister)

* Fri Apr  4 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.2-1
- Upstream release
- Modification of gnuradio-3.1.2-gcc34.patch to the new release

* Thu Mar 27 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.1-4
- Moving libusrp to gnuradio package

* Wed Feb 20 2008 Marek Mahut <mmahut@fedoraproject.org> - 3.1.1-2
- Upstream release
- Spec file rewrite

* Mon Mar 12 2007 Trond Danielsen <trond.danielsen@gmail.com> - 3.0.3-1
- Initial version.

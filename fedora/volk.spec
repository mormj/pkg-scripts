%define __distro_section %{?distro_section:%distro_section}%{?!distro_section:core}
%define mklibname(ds)  %{_lib}%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}
%define mkrel(c:) %{-c: 0.%{-c*}.}%{1}%{?subrel:.%subrel}%{?dist:%dist}%{?!dist:%__dist_ident}%([ "%{__distro_section}" != "core" ] && echo .%__distro_section)


%define major	2
%define libvolk %mklibname %{name} %{major}
%define devvolk %mklibname %{name} -d

Name:		volk
Version:	2.2.1
Release:	%mkrel 1
Summary:	Vector-Optimized Library of Kernels
Group:		Communications/Radio
License:	GPLv3+
URL:		http://libvolk.org
Source0:	https://github.com/gnuradio/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Requires(pre):	shadow-utils
BuildRequires:	cmake, cppunit-devel
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3-mako
BuildRequires:	python3-six
Requires:	%{libvolk} = %{version}-%{release}

%description
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.
This is now packaged independently of GNU Radio.

%files
%{_bindir}/volk_modtool
%{_bindir}/volk_profile
%{_bindir}/volk-config-info
%{python3_sitelib}/volk_modtool/*

############################
%package -n %{libvolk}
Summary:	Volk libraries
Group:		System/Libraries
Obsoletes:	%{_lib}gnuradio-volk0 < 3.8
Conflicts:	%{_lib}gnuradio-volk0 < 3.8

%description -n %{libvolk}
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.

%files -n %{libvolk}
%{_libdir}/libvolk.so.%{major}{,.*}

############################
%package -n %{devvolk}
Summary:	Volk devel files
Group:		Development/Other
Requires:	%{libvolk} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gnuradio-volk-devel < 3.8
Conflicts:	%{_lib}gnuradio-volk-devel < 3.8

%description -n %{devvolk}
This package contains header files needed by developers.

%files -n %{devvolk}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/volk.pc
%{_libdir}/libvolk.so
%{_libdir}/cmake/volk

###########################
%prep
%autosetup -p1

%build
%cmake \
	-DPYTHON_EXECUTABLE=%{_bindir}/python3 \
	-DVOLK_PYTHON_DIR:PATH=%{python3_sitelib} \
	-DENABLE_PROFILING=OFF
%cmake_build

%install
%cmake_install


%changelog
* Thu Mar 19 2020 barjac <barjac> 2.2.1-1.mga8
+ Revision: 1557874
- new version 2.2.1

* Wed Feb 19 2020 umeabot <umeabot> 2.0.0-3.mga8
+ Revision: 1544940
- Mageia 8 Mass Rebuild

* Sun Jan 26 2020 wally <wally> 2.0.0-2.mga8
+ Revision: 1483449
- rebuild for boost 1.72.0
- build with new cmake macros

* Wed Sep 18 2019 barjac <barjac> 2.0.0-1.mga8
+ Revision: 1443682
- Fix python lib path
- add BRs orc, doxygen
- disable profiling
- adjust files lists and add obsoletes
- fix some typos
- new package volk

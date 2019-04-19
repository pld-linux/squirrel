#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	High level imperative/OO programming language
Summary(pl.UTF-8):	Wysokopoziomowy imperatywny/zorientowany obiektowo język programowania
Name:		squirrel
Version:	2.2.5
Release:	1
License:	Zlib
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/squirrel/%{name}_%{version}_stable.tar.gz
# Source0-md5:	35f97d933d46e2b5d54e0c0f2eccfa4a
Patch0:		%{name}-autotools.patch
Patch1:		%{name}-mem.patch
URL:		http://squirrel-lang.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Squirrel is a high level imperative/OO programming language, designed
to be a powerful scripting tool that fits in the size, memory
bandwidth, and real-time requirements of applications like games.

%description -l pl.UTF-8
Squirrel to wysokopoziomowy, imperatywny, zorientowany obiektowo język
programowania, zaprojektowany jako potężne narzędzie do skryptów,
nadający się pod względem rozmiaru, wykorzystania pamięci i wymagań
czasu rzeczywistego do takich zastosowań, jak gry.

%package devel
Summary:	Development files needed to use Squirrel libraries
Summary(pl.UTF-8):	Pliki programistyczne potrzebne do korzystania z bibliotek Squirrela
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files needed to use Squirrel libraries.

%description devel -l pl.UTF-8
Pliki programistyczne potrzebne do korzystania z bibliotek Squirrela.

%package static
Summary:	Static Squirrel libraries
Summary(pl.UTF-8):	Statyczne biblioteki Squirrela
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Squirrel libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Squirrela.

%prep
%setup -q -c
cd SQUIRREL2
%patch0 -p1
%patch1 -p1

# fix extension for autotools
%{__mv} sq/sq.c sq/sq.cpp

%build
cd SQUIRREL2
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C SQUIRREL2 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc SQUIRREL2/{README,HISTORY,COPYRIGHT}
%attr(755,root,root) %{_bindir}/sq
%attr(755,root,root) %{_libdir}/libsqstdlib-%{version}.so
%attr(755,root,root) %{_libdir}/libsquirrel-%{version}.so

%files devel
%defattr(644,root,root,755)
%doc SQUIRREL2/doc/*.pdf
%attr(755,root,root) %{_libdir}/libsqstdlib.so
%attr(755,root,root) %{_libdir}/libsquirrel.so
%{_libdir}/libsqstdlib.la
%{_libdir}/libsquirrel.la
%{_includedir}/squirrel
%{_pkgconfigdir}/squirrel.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsquirrel.a
%{_libdir}/libsqstdlib.a
%endif

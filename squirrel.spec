#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	High level imperative/OO programming language
Name:		squirrel
Version:	2.2.4
Release:	1
License:	zlib
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/squirrel/%{name}_%{version}_stable.tar.gz
# Source0-md5:	e411dfd1bcc5220aa80de53e4a5f094d
Patch0:		%{name}-autotools.patch
URL:		http://squirrel-lang.org/
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Squirrel is a high level imperative/OO programming language, designed
to be a powerful scripting tool that fits in the size, memory
bandwidth, and real-time requirements of applications like games.

%package devel
Summary:	Development files needed to use Squirrel libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files needed to use Squirrel libraries.

%package static
Summary:	Static libsquirrel library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libsquirrel library.

%prep
%setup -q -c
%patch0 -p1

# fix extension for autotools
cd SQUIRREL2
mv sq/sq.c sq/sq.cpp

%build
cd SQUIRREL2
sh autogen.sh
%configure
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd SQUIRREL2
%{__make} install \
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
%{_libdir}/libsqstdlib.so
%{_libdir}/libsquirrel.so
%{_libdir}/libsqstdlib.la
%{_libdir}/libsquirrel.la
%{_includedir}/squirrel

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsquirrel.a
%{_libdir}/libsqstdlib.a
%endif

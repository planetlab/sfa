%define url $URL: svn+ssh://svn.planet-lab.org/svn/geniwrapper/trunk/geniwrapper.spec $

%define name sfa
%define version 0.8
%define taglevel 0

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}
%global python_sitearch	%( python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" )
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %(echo %{url} | cut -d ' ' -f 2)

BuildRequires: make
Requires: python
Requires: pyOpenSSL >= 0.7
Requires: m2crypto

Summary: the GENI python libraries
Group: Applications/System

%package plc
Summary: the GENI wrapper arounf MyPLC
Group: Applications/System
Requires: sfa

%package client
Summary: the GENI experimenter-side CLI
Group: Applications/System
Requires: sfa

%description
This package provides the python libraries that the Geni implementation requires

%description plc
Geniwrapper implements the Geni interface which serves as a layer
between the existing PlanetLab interfaces and the Geni API.

%description client
This package provides the client side of the Geni API, in particular
sfi.py, together with other utilities.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{python_sitelib}/*
/usr/share/keyconvert/
/var/www/html/wsdl/sfa.wsdl

%files plc
%defattr(-,root,root)
%config (noreplace) /etc/geni/geni_config
%config (noreplace) /etc/geni/aggregates.xml
%config (noreplace) /etc/geni/registries.xml
/etc/init.d/geni
%{_bindir}/geni-config-tty
%{_bindir}/gimport.py*
%{_bindir}/plc.py*

%files client
%config (noreplace) /etc/geni/sfi_config
%{_bindir}/sfi.py*
%{_bindir}/getNodes.py*
%{_bindir}/getRecord.py*
%{_bindir}/setRecord.py*
%{_bindir}/genidump.py*

%post plc
chkconfig --add geni

%changelog
* Wed Jul 01 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-7
- snapshot for reproducible builds

* Thu Jun 25 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-6
- snapshot for the convenience of alpha users

* Tue Jun 16 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-5
- build fix - keyconvert was getting installed in /usr/share/keyconvert/keyconvert

* Tue Jun 16 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-4
- ongoing work - snapshot for 4.3-rc9

* Wed Jun 03 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-3
- various fixes

* Sat May 30 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.2-2
- bugfixes - still a work in progress

* Fri May 18 2009 Baris Metin <tmetin@sophia.inria.fr>
- initial package


%define module_current_branch 0.2

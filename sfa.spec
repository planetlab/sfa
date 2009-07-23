%define url $URL: svn+ssh://svn.planet-lab.org/svn/geniwrapper/trunk/geniwrapper.spec $

%define name sfa
%define version 0.8
%define taglevel 6

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

Summary: the SFA python libraries
Group: Applications/System

%package plc
Summary: the SFA wrapper arounf MyPLC
Group: Applications/System
Requires: sfa

%package client
Summary: the SFA experimenter-side CLI
Group: Applications/System
Requires: sfa

%description
This package provides the python libraries that the SFA implementation requires

%description plc
Geniwrapper implements the SFA interface which serves as a layer
between the existing PlanetLab interfaces and the SFA API.

%description client
This package provides the client side of the SFA API, in particular
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
/usr/bin/keyconvert
/var/www/html/wsdl/*.wsdl

%files plc
%defattr(-,root,root)
%config (noreplace) /etc/sfa/sfa_config
%config (noreplace) /etc/sfa/aggregates.xml
%config (noreplace) /etc/sfa/registries.xml
/etc/init.d/sfa
%{_bindir}/sfa-config-tty
%{_bindir}/sfa-import-plc.py*
%{_bindir}/sfa-nuke-plc.py*
%{_bindir}/sfa-server.py*

%files client
%config (noreplace) /etc/sfa/sfi_config
%{_bindir}/sfi.py*
%{_bindir}/getNodes.py*
%{_bindir}/getRecord.py*
%{_bindir}/setRecord.py*
%{_bindir}/genidump.py*

%pre plc
[ -f %{_sysconfdir}/init.d/sfa ] && service sfa stop ||:

%post plc
chkconfig --add sfa

%changelog
* Thu Jul 23 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-6
- snapshot after the GEC5 demo
- should be the last tag set in the geniwrapper module, are we are now moving to the sfa module

* Wed Jul 15 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-5
- snapshot july 15 - has gone through superficial manual testing
- hopefully a good basis for gec5 demo
- multi-dir sfi client tested as well

* Wed Jul 08 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-4
- rename geniwrapper.spec into sfa.spec

* Wed Jul 08 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-3
- clean up in xmlrpc/soap, --protocol option to chose between both
- keyconvert packaged in /usr/bin, no /usr/share/keyconvert anymore
- hopefully more helpful context in case of crashes when importing
- bugfixes for using only /etc/sfa for site-dep files
- bugfixes in wsdl generation

* Mon Jul 06 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-2
- cleanup of the config area; no dependency to a PLC config anymore as sfa can be run in standalone
- config variables in sfa_config now start with SFA_ and not GENI_
- config.py can be loaded even with no config present

* Sun Jul 05 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - geniwrapper-0.8-1
- first step for cleanup and reorganization
- mass-renaming from geni to sfa (some are still needed)
- sfa/trust implements the security architecture

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


%define url $URL: svn+ssh://svn.planet-lab.org/svn/geniwrapper/trunk/geniwrapper.spec $

%define name geniwrapper
%define version 0.8
%define taglevel 0

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}
%global python_sitearch	%( python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" )

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


Summary: Geniwrapper
Group: Applications/System

%description
Geniwrapper description...

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"

# hack to add installed files to the package
python -c "print '\n'.join(['%s*'%i.strip() for i in open('GENI_INSTALLED_FILES').readlines() if not i.strip().endswith('.pyc')])" |uniq > GENI_INSTALLED_FILES.all


%clean
rm -rf $RPM_BUILD_ROOT

%files -f GENI_INSTALLED_FILES.all
%defattr(-,root,root)
/usr/share/keyconvert
%config (noreplace) /etc/geni/geni_config
%config (noreplace) /etc/geni/sfi_config
%config (noreplace) /etc/geni/aggregates.xml
%config (noreplace) /etc/geni/registries.xml

%post
chmod 0744 /etc/init.d/geniwrapper

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

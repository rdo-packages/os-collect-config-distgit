# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:			os-collect-config
Version:		XXX
Release:		XXX
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
Source1:		os-collect-config.service
Source2:		os-collect-config.conf

BuildArch:		noarch
BuildRequires:		systemd
Requires:		os-refresh-config

BuildRequires:		python%{pydefault}-setuptools
BuildRequires:		python%{pydefault}-devel
BuildRequires:		python%{pydefault}-pbr

Requires:		python%{pydefault}-pbr
Requires:		python%{pydefault}-eventlet
Requires:		python%{pydefault}-heatclient >= 1.10.0
Requires:		python%{pydefault}-zaqarclient >= 1.0.0
Requires:		python%{pydefault}-keystoneclient >= 1:3.8.0
Requires:		python%{pydefault}-requests
Requires:		python%{pydefault}-iso8601
Requires:		python%{pydefault}-six
Requires:		python%{pydefault}-oslo-config >= 2:5.2.0
Requires:		python%{pydefault}-oslo-log >= 3.36.0

%if %{pydefault} == 2
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python-lxml
%else
Requires:		python%{pydefault}-anyjson
Requires:		python%{pydefault}-dogpile-cache
Requires:		python%{pydefault}-lxml
%endif
%{?systemd_requires}

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%build
%{pydefault_build}

%install
%{pydefault_install}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/local-data

# Delete tests
rm -fr %{buildroot}%{pydefault_sitelib}/os_collect_config/tests

%post
%systemd_post os-collect-config.service

%preun
%systemd_preun os-collect-config.service

%postun
%systemd_postun os-collect-config.service

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-collect-config
%config(noreplace) %attr(-, root, root) %{_sysconfdir}/os-collect-config.conf
%{_unitdir}/os-collect-config.service
%{_sharedstatedir}/%{name}/local-data
%{pydefault_sitelib}/os_collect_config*

%changelog

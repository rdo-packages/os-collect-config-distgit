# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:			os-collect-config
Version:		10.3.1
Release:		1%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
Source1:		os-collect-config.service
Source2:		os-collect-config.conf

BuildArch:		noarch
BuildRequires:		systemd
Requires:		os-refresh-config

BuildRequires:		python%{pyver}-setuptools
BuildRequires:		python%{pyver}-devel
BuildRequires:		python%{pyver}-pbr

Requires:		python%{pyver}-pbr
Requires:		python%{pyver}-eventlet
Requires:		python%{pyver}-heatclient >= 1.10.0
Requires:		python%{pyver}-zaqarclient >= 1.0.0
Requires:		python%{pyver}-keystoneclient >= 1:3.8.0
Requires:		python%{pyver}-requests
Requires:		python%{pyver}-iso8601
Requires:		python%{pyver}-six
Requires:		python%{pyver}-oslo-config >= 2:5.2.0
Requires:		python%{pyver}-oslo-log >= 3.36.0

%if %{pyver} == 2
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python-lxml
%else
Requires:		python%{pyver}-anyjson
Requires:		python%{pyver}-dogpile-cache
Requires:		python%{pyver}-lxml
%endif
%{?systemd_requires}

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%build
%{pyver_build}

%install
%{pyver_install}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/local-data

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/os_collect_config/tests

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
%{pyver_sitelib}/os_collect_config*

%changelog
* Thu Dec 12 2019 RDO <dev@lists.rdoproject.org> 10.3.1-1
- Update to 10.3.1

* Thu Apr 18 2019 RDO <dev@lists.rdoproject.org> 10.3.0-1
- Update to 10.3.0

* Tue Apr 02 2019 RDO <dev@lists.rdoproject.org> 10.2.0-1
- Update to 10.2.0


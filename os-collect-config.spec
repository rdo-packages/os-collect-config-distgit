
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:			os-collect-config
Version:		11.0.1
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

BuildRequires:		python3-setuptools
BuildRequires:		python3-devel
BuildRequires:		python3-pbr

Requires:		python3-pbr
Requires:		python3-eventlet
Requires:		python3-heatclient >= 1.10.0
Requires:		python3-zaqarclient >= 1.0.0
Requires:		python3-keystoneclient >= 1:3.8.0
Requires:		python3-requests
Requires:		python3-iso8601
Requires:		python3-six
Requires:		python3-oslo-config >= 2:5.2.0
Requires:		python3-oslo-log >= 3.36.0

Requires:		python3-anyjson
Requires:		python3-dogpile-cache
Requires:		python3-lxml
%{?systemd_requires}

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%build
%{py3_build}

%install
%{py3_install}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/local-data

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/os_collect_config/tests

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
%{python3_sitelib}/os_collect_config*

%changelog
* Mon Oct 05 2020 RDO <dev@lists.rdoproject.org> 11.0.1-1
- Update to 11.0.1

* Thu May 07 2020 RDO <dev@lists.rdoproject.org> 11.0.0-1
- Update to 11.0.0


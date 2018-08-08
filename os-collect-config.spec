%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 28
%global with_python3 1
%endif

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

%if 0%{?with_python3} == 0
# begin python2 requirements
BuildRequires:		python2-setuptools
BuildRequires:		python2-devel
BuildRequires:		python2-pbr

Requires:		python2-pbr
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python2-eventlet
Requires:		python2-heatclient >= 1.10.0
Requires:		python2-zaqarclient >= 1.0.0
Requires:		python2-keystoneclient >= 1:3.8.0
Requires:		python2-requests
Requires:		python2-iso8601
Requires:		python-lxml
Requires:		python2-six
Requires:		python2-oslo-config >= 2:5.1.0
Requires:		python2-oslo-log >= 3.36.0
# end python2 requirements
%else
# begin python3 requirements
BuildRequires:		python3-setuptools
BuildRequires:		python3-devel
BuildRequires:		python3-pbr

Requires:		python3-pbr
Requires:		python3-anyjson
Requires:		python3-dogpile-cache
Requires:		python3-eventlet
Requires:		python3-heatclient >= 1.10.0
Requires:		python3-zaqarclient >= 1.0.0
Requires:		python3-keystoneclient >= 1:3.8.0
Requires:		python3-requests
Requires:		python3-iso8601
Requires:		python3-lxml
Requires:		python3-six
Requires:		python3-oslo-config >= 2:5.1.0
Requires:		python3-oslo-log >= 3.36.0
# end python3 requirements
%endif
%{?systemd_requires}

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%build
%if 0%{?with_python3} == 0
%{py2_build}
%else
%{py3_build}
%endif

%install
%if 0%{?with_python3} == 0
%{py2_install}
%else
%{py3_install}
%endif
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/local-data

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/os_collect_config/tests

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
%if 0%{?with_python3} == 0
%{python2_sitelib}/os_collect_config*
%else
%{python3_sitelib}/os_collect_config*
%endif

%changelog

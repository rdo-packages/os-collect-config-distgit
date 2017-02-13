%global milestone .0rc1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:			os-collect-config
Version:		6.0.0
Release:		0.1%{?milestone}%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
#
# patches_base=6.0.0.0rc1
#

Source1:		os-collect-config.service
Source2:		os-collect-config.conf

BuildArch:		noarch
BuildRequires:		python-setuptools
BuildRequires:		python2-devel
BuildRequires:		systemd
BuildRequires:		python-pbr

Requires:		python-pbr
Requires:		python-setuptools
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python-eventlet
Requires:		python-heatclient
Requires:		python-zaqarclient
Requires:		os-refresh-config
Requires:		python-keystoneclient
Requires:		python-requests
Requires:		python-iso8601
Requires:		python-lxml
Requires:		python-six
Requires:		python-oslo-config
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires:		python-oslo-log >= 3.11.0

%description
Service to collect openstack heat metadata.

%prep

%setup -q -n %{name}-%{upstream_version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf

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
%{python_sitelib}/os_collect_config*
%{_unitdir}/os-collect-config.service

%changelog
* Mon Feb 13 2017 Alfredo Moralejo <amoralej@redhat.com> 6.0.0-0.1.0rc1
- Update to 6.0.0.0rc1


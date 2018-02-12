%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:			os-collect-config
Version:		7.2.2
Release:		1%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		ASL 2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
Source1:		os-collect-config.service
Source2:		os-collect-config.conf

BuildArch:		noarch
BuildRequires:		python-setuptools
BuildRequires:		python2-devel
BuildRequires:		systemd
BuildRequires:		python-pbr

Requires:		python-pbr
Requires:		python-anyjson
Requires:		python-dogpile-cache
Requires:		python-eventlet
Requires:		python-heatclient >= 1.6.1
Requires:		python-zaqarclient >= 1.0.0
Requires:		os-refresh-config
Requires:		python-keystoneclient >= 1:3.8.0
Requires:		python-requests
Requires:		python-iso8601
Requires:		python-lxml
Requires:		python-six
Requires:		python-oslo-config >= 2:4.0.0
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Requires:		python-oslo-log >= 3.22.0

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
* Mon Feb 12 2018 RDO <dev@lists.rdoproject.org> 7.2.2-1
- Update to 7.2.2

* Wed Nov 22 2017 RDO <dev@lists.rdoproject.org> 7.2.1-1
- Update to 7.2.1

* Sun Sep 10 2017 rdo-trunk <javier.pena@redhat.com> 7.2.0-1
- Update to 7.2.0

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 7.1.0-1
- Update to 7.1.0


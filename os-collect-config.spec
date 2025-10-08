%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate sphinx openstackdocstheme

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:			os-collect-config
Version:		14.0.0
Release:		1%{?dist}
Summary:		Collect and cache metadata running hooks on changes

License:		Apache-2.0
URL:			http://pypi.python.org/pypi/%{name}
Source0:		https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
Source1:		os-collect-config.service
Source2:		os-collect-config.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:		noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:		systemd
BuildRequires:		python3-devel
BuildRequires:		pyproject-rpm-macros
# Needed fot the tests setting specific locale
BuildRequires:		glibc-langpack-en

Requires:		os-refresh-config

%{?systemd_requires}

%description
Service to collect openstack heat metadata.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif

%setup -q -n %{name}-%{upstream_version}

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/os-collect-config.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/os-collect-config.conf
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/local-data

%check
%tox -e %{default_toxenv}

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
%exclude %{python3_sitelib}/os_collect_config/tests

%changelog
* Fri Apr 19 2024 RDO <dev@lists.rdoproject.org> 14.0.0-1
- Update to 14.0.0

* Tue Apr 16 2024 RDO <dev@lists.rdoproject.org> 13.2.0-1
- Update to 13.2.0

# REMOVEME: error caused by commit https://opendev.org/openstack/os-collect-config/commit/146c0407ff97f08aa9f2dd55d9b2d56eb1568218

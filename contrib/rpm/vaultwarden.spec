%define __spec_install_post %{nil}
%define __os_install_post %{_dbpath}/brp-compress
%define debug_package %{nil}

Name: vaultwarden
Summary: 
Version: 1.26.0
Release: 1
License: GPLv3
Group: Applications/System
Source0: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: systemd

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
%{summary}

%prep
%setup -q

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * %{buildroot}
mkdir -p %{buildroot}%{_localstatedir}/lib/vaultwarden/

%clean
rm -rf %{buildroot}

%systemd_post vaultwarden.service

%preun
%systemd_preun vaultwarden.service

%postun
%systemd_postun_with_restart vaultwarden.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_unitdir}/vaultwarden.service
%attr(0755,vaultwarden,root) %dir %{_localstatedir}/lib/vaultwarden

%pre
getent group vaultwarden >/dev/null || groupadd -r vaultwarden
getent passwd vaultwarden >/dev/null || \
    useradd -r -g vaultwarden -d / -s /sbin/nologin vaultwarden
exit 0

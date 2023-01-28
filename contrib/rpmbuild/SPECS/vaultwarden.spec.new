%define pkg_name vaultwarden
%define _unpackaged_files_terminate_build 0

Name:      %{pkg_name}
Version:   1.26.0
Release:   1.2
License:   GPL-3.0
Summary:   Unofficial Bitwarden compatible server written in Rust
Url:       https://github.com/dani-garcia/vaultwarden
Group:     Applications/System
Source0:   %{pkg_name}-%{version}.tar.gz
Source1:   vendor.tar.xz
Source2:   rust-1.64.0-x86_64-unknown-linux-gnu.tar.gz
Source3:   cargo_config
Source10:  %{pkg_name}.service
Source11:  %{pkg_name}.logrotate
Source100: %{pkg_name}.cfg

BuildRequires: systemd
BuildRequires: tar
BuildRequires: sed
BuildRequires: git
BuildRequires: pkgconfig(openssl)
%if 0%{?fedora} || 0%{?rhel_version} > 700 || 0%{?centos_version} > 700
BuildRequires: sqlite-devel
BuildRequires: mariadb-connector-c-devel
BuildRequires: libpq-devel
%endif
%if 0%{?centos_version} == 700 || 0%{?rhel_version} == 700
BuildRequires: sqlite-devel
BuildRequires: mariadb-devel
%endif
%if 0%{?sle_version} || 0%{?suse_version}
BuildRequires: sqlite3-devel
BuildRequires: libmariadb-devel
BuildRequires: libpqxx-devel
%endif
%if 0%{?centos_version} == 700
BuildRequires: libpqxx-devel
%endif
%if 0%{?sle_version} || 0%{?rhel_version} == 700
BuildRequires: postgresql-devel
%endif

%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
Requires(pre): shadow-utils
%else
Requires(pre): shadow
%endif
Requires: systemd
%if 0%{?fedora} || 0%{?rhel_version} > 700 || 0%{?centos_version} > 700
Requires: mariadb-connector-c
Requires: libpq
%endif
%if 0%{?centos_version} == 700 || 0%{?rhel_version} == 700
Requires: postgresql-libs
Requires: mariadb-libs
%endif
%if 0%{?sle_version} || 0%{?suse_version}
Requires: libmariadb3
Requires: libpq5
%endif


Conflicts:  bitwarden
Conflicts:  bitwarden-rs
%if ! 0%{?rhel_version} == 700 && ! 0%{?centos_version} == 700
Recommends: %{pkg_name}-webvault
Suggests:   logrotate
Provides:   bitwarden
Provides:   bitwarden-rs
%endif

BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-root
%{?systemd_ordering}

%description
Alternative implementation of the Bitwarden server API written in Rust and compatible with upstream Bitwarden clients, perfect for self-hosted deployment where running the official resource-heavy service might not be ideal.

%prep
%{__tar} -xf %{SOURCE0} --strip-components 1
%{__tar} -xf %{SOURCE1}
%{__tar} -xf %{SOURCE2}
#-e %{buildroot}/.cargo && rm -rf %{buildroot}/.cargo 
mkdir -p .cargo
cp %{SOURCE3} .cargo/config

%build
./rust*/install.sh --components=cargo,rustc,rust-std-x86_64-unknown-linux-gnu --disable-ldconfig --prefix=%{buildroot}/rust
export PATH=%{buildroot}/rust/bin:$PATH
#cargo build --features sqlite,mysql,postgresql --offline --release --target-dir %{_builddir}/%{pkg_name}-%{version}/target
cargo build --features sqlite,mysql --offline --release --target-dir %{_builddir}/%{pkg_name}-%{version}/target

%{__sed} -i 's#<sed-target-1>#%{_bindir}#' %{SOURCE10}
%{__sed} -i 's#<sed-target-2>#%{_sysconfdir}/%{pkg_name}#' %{SOURCE10}
%{__sed} -i 's#<sed-target-3>#%{_sharedstatedir}/%{pkg_name}#' %{SOURCE10}
%{__sed} -i 's#<sed-target-4>#%{_sysconfdir}/%{pkg_name}#' %{SOURCE10}
%{__sed} -i 's#<sed-target-1>#%{_localstatedir}/log/%{pkg_name}#' %{SOURCE11}
%{__sed} -i 's#<sed-target-1>#%{_sharedstatedir}/%{pkg_name}#' %{SOURCE100}
%{__sed} -i 's#<sed-target-2>#%{_datarootdir}/%{pkg_name}/web-vault#' %{SOURCE100}
%{__sed} -i 's#<sed-target-3>#%{_localstatedir}/log/%{pkg_name}#' %{SOURCE100}

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 750 -d %{buildroot}%{_sharedstatedir}/%{pkg_name}
install -m 750 -d %{buildroot}%{_localstatedir}/log/%{pkg_name}
install -m 755 -d %{buildroot}%{_sbindir}
install -m 750 -d %{buildroot}%{_sysconfdir}/%{pkg_name}

install -D -m 750 %{_builddir}/%{pkg_name}-%{version}/target/release/%{pkg_name} %{buildroot}%{_bindir}/%{pkg_name}
install -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{pkg_name}.service
install -D -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
install -D -m 640 %{SOURCE100} %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.cfg

%{__ln_s} -f %{_sbindir}/service %{buildroot}%{_sbindir}/rc%{pkg_name}

%check


%pre
%systemd_pre %{pkg_name}.service
getent group %{pkg_name} >/dev/null || groupadd -r %{pkg_name}
getent passwd %{pkg_name} >/dev/null || useradd -r -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name} -s /sbin/nologin -c "user for %{pkg_name}" %{pkg_name}
exit 0

%preun
%systemd_preun %{pkg_name}.service

%post
%systemd_post %{pkg_name}.service
systemctl enable %{pkg_name}.service
systemctl start %{pkg_name}.service

%postun
%systemd_postun %{pkg_name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{pkg_name}.service
%{_sbindir}/rc%{pkg_name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%dir %attr(750,%{pkg_name},%{pkg_name}) %{_sysconfdir}/%{pkg_name}
%config(noreplace) %attr(-,%{pkg_name},%{pkg_name}) %{_sysconfdir}/%{pkg_name}/*
%dir %attr(750,%{pkg_name},%{pkg_name}) %{_sharedstatedir}/%{pkg_name}/
%dir %attr(750,%{pkg_name},%{pkg_name}) %{_localstatedir}/log/%{pkg_name}/
%attr(550,%{pkg_name},%{pkg_name}) %{_bindir}/%{pkg_name}
%changelog
* Tue Oct 18 2022 Julian Röder <obs@masgalor.de>
- Update to version 1.26.0
  * Fix uploads from mobile clients (and dep updates) by @BlackDex in #2675
  * Add support for send v2 API endpoints by @BlackDex in #2756
  * External Links | Optimize behavior by @Fvbor in #2693
  * Add Org user revoke feature by @BlackDex in #2698
  * Change the handling of login errors. by @BlackDex in #2729
  * Added support for web-vault v2022.9 by @BlackDex in #2732
  * add not_found catcher for 404 errors by @stefan0xC in #2768
  * Fix issue 2737, unable to create org by @BlackDex in #2738
  * Rename/Fix revoke/restore endpoints by @BlackDex in #2739
  * Update CSP for DuckDuckGo email forwarding by @jjlin in #2812
  * check if data folder is a writable directory by @stefan0xC in #2811
  * fix: tooltip typo by @djbrownbear in #2746
  * Update libraries and Rust version by @BlackDex in #2758
  * Fix organization vault export by @BlackDex in #2765
  * allow the removal of non-confirmed owners by @stefan0xC in #2772
  * v2022.9.2 expects a json response while registering by @stefan0xC in #2803
  * make invitation expiration time configurable by @stefan0xC in #2805
  * return more descriptive JWT validation messages by @stefan0xC in #2806
  * Add CreationDate to cipher response JSON by @jjlin in #2813
- Improve systemd-integration with some distributions.
* Fri Oct  7 2022 Julian Röder <obs@masgalor.de>
- Improve the build environment
  * Requirements that were only introduced to satisfy the build service were removed.
    Conflitcs and choices are now resolved within the project configuration.
  * The rust-setup was optimized to skip unnecessary components and configurations.
* Thu Jul 28 2022 Julian Röder <obs@masgalor.de>
- Update to version 1.25.2
  * Fix persistent folder check within containers by @BlackDex in #2631
  * Mitigate attachment/send upload issues by @BlackDex in #2650
  * Fix issue with CSP and icon redirects by @BlackDex in #2624
* Mon Jul 18 2022 Julian Röder <obs@masgalor.de>
- Change the buildrecipe to build all binaries on the intended target system, instead of reusing prebuilt binaries.
- Update to version 1.25.1
  * Sync global_domains.json by @jjlin in #2555
  * Add TMP_FOLDER to .env.template by @fox34 in #2489
  * Allow FireFox relay in CSP. by @BlackDex in #2565
  * Fix hidden ciphers within organizational view. by @BlackDex in #2567
  * Add password_hints_allowed config option by @jjlin in #2586
  * Fall back to move_copy_to if persist_to fails while saving uploaded files. by @ruifung in #2605
  * Swap Websocket crate from ws to tungstenite, which is more maintained, supports async, and removes around 20 old duplicate versions of used crates by @dani-garcia
  * Add a persistent volume check. by @BlackDex in #2501, #2507
  * Adding "UserEnabled" and "CreatedAt" member to the json output of a User by @Lowaiz in #2523
  * Bump lettre to 0.10.0-rc.7 by @paolobarbolini in #2531
  * Small email sending code improvements by @paolobarbolini in #2532
  * A little depreciation change by @binlab in #2556
  * Fix identicons not always working by @BlackDex in #2571
  * Small change in log-level for better debugging by @BlackDex in #2577
  * Address inconsistency v{version} with and without a v in the version with most recent updates. by @nneul in #2595
  * Bump openssl-src from 111.21.0+1.1.1p to 111.22.0+1.1.1q by @dependabot in #2599
  * Add more clippy checks for better code/readability by @BlackDex in #2611
  * Update deps, misc fixes and updates, small improvements on favicons and fix file-uploads by @BlackDex in #2543, #2568, #2619
* Fri Jun  3 2022 Julian Röder <obs@masgalor.de>
- Update to version 1.25.0
  * Update Rocket to 0.5 and async, and compile on stable by @dani-garcia in #2276
  * Update async to prepare for main merge + several updates by @BlackDex in #2292
  * Add IP address to missing/invalid password message for Sends by @jaen in #2313
  * Add support for custom .env file path by @TinfoilSubmarine in #2315
  * Added autofocus to pw field on admin login page by @taylorwmj in #2328
  * Update login API code and update crates to fix CVE by @BlackDex in #2354
  * Several updates and fixes by @BlackDex in #2379
  * disable legacy X-XSS-Protection feature by @Wonderfall in #2380
  * Fix building mimalloc on armv6 by @BlackDex in #2397
  * Remove u2f implementation by @BlackDex in #2398
  * Sync global_domains.json by @jjlin in #2400
  * Add /api/{alive,now,version} endpoints by @jjlin in #2433
  * Improve sync speed and updated dep. versions by @BlackDex in #2429
  * Database connection init by @jjlin in #2440
  * Fix upload limits and disable color logs by @BlackDex in #2480
* Mon Jan 31 2022 Julian Röder <obs@masgalor.de>
- Update to version 1.24.0
  * Add support for external icon services by @jjlin in #2158
  * Add config option to set the HTTP redirect code for external icons by @jjlin in #2188
  * Add support for legacy HTTP 301/302 redirects for external icons by @jjlin in #2218
  * Add support for API keys by @jjlin in #2245
  * Basic ratelimit for user login (including 2FA) and admin login by @dani-garcia in #2165
  * Upgrade Feature-Policy to Permissions-Policy by @iamdoubz in #2228
  * Set Expires header when caching responses by @RealOrangeOne in #2182
  * Increase length limit for email token generation by @jjlin in #2257
  * Small changes to icon log messages. by @BlackDex in #2170
  * Bump rust version to mitigate CVE-2022-21658 by @dscottboggs in #2255
  * Fixed #2151 by @BlackDex in #2169
  * Fixed issue #2154 by @BlackDex in #2194
  * Fix issue with Bitwarden CLI. by @BlackDex in #2197
  * Fix emergency access invites for new users by @BlackDex in #2217
  * Sync global_domains.json by @jjlin in #2156
  * Sync global_domains.json by @jjlin in #2171
- Complete default config file
* Wed Dec 15 2021 Julian Röder <obs@masgalor.de>
- Update to version 1.23.1
  * Add email notifications for incomplete 2FA logins by @jjlin in #2067
  * Fix conflict resolution logic for read_only and hide_passwords flags by @jjlin in #2073
  * Fix missing encrypted key after emergency access reject by @jjlin in #2078
  * Fix PostgreSQL migration by @jjlin in #2080
  * Macro recursion decrease and other optimizations by @BlackDex in #2084
  * Enabled trust-dns and some updates. by @BlackDex in #2125
* Thu Oct 21 2021 Julian Röder <obs@masgalor.de>
- Update to version 1.23.0
  * Added emergency access feature
  * Can be disabled setting EMERGENCY_ACCESS_ALLOWED=false
  * Added support for single organization policy
  * Fixed incorrect webauthn origin
  * Enforce personal ownership policy on imports
  * Fixed issue using uppercase characters on emails
  * Added organization bulk user management actions (reinvite/confirm/delete)
  * Removed limmit that disabled sending ciphers with attachments
  * Disabled enforcing of two factor organization policy on users that haven't been accepted yet
  * Updated icon fetching to make it work on unicode websites
  * Added database connection check to /alive endpoint
  * Updated dependencies
* Tue Jul 27 2021 Julian Röder <obs@masgalor.de>
- Update to version 1.22.2
  * Enforce 2FA policy in organizations.
  * Protect send routes against a possible path traversal attack.
  * Disable show_password_hint by default, it still can be enabled in the admin panel or with environment variables.
  * Disable user verification enforcement in Webauthn, which would make some users unable to login.
  * Fix issue that wouldn't correctly delete Webauthn Key.
  * Added Edge extension support for Webauthn.
* Thu Jul  1 2021 Julian Röder <obs@masgalor.de>
- Update to version 1.22.1
  * Added sends_allowed option to disable Send functionality.
  * Added support for hiding the senders email address.
  * Added Send options policy.
  * Added support for password reprompt.
  * Switched to the new attachment download API.
  * Send download links use a token system to limit their downloads.
  * Updates to the icon fetching.
  * Support for webauthn.
  * The admin page now shows which variables are overridden.
  * Updated dependencies and docker base images.
  * Now RSA keys are generated with the included openssl instead of calling to the openssl binary.
- Remove OpenSSL as dependency as it is no longer needed.
* Wed May 26 2021 Julian Röder <obs@masgalor.de>
- Add support for mysql und postgresql
* Mon May  3 2021 Julian Röder <obs@masgalor.de>
- Improves package relations on debian-based distributions
* Fri Apr 30 2021 Julian Röder <obs@masgalor.de>
- Project renamed to Vaultwarden
- Update to version 1.21.0
  * Add support for enabling auto-deletion of trash items after X days, disabled by default
  * Set TRASH_AUTO_DELETE_DAYS to a positive value to enable this functionality
  * You can also configure how often this process runs, using cron sintax with the variable TRASH_PURGE_SCHEDULE
  * Updates to the icon fetching, making it more reliable in detecting icon types
  * Updated admin page, improving version checks and SQLite backup feature

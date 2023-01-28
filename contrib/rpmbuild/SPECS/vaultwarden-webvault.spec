%define pkg_name vaultwarden

Name:       %{pkg_name}-webvault
Version:    2022.10.2
Release:    1.3
License:    GPL-3.0
Summary:    Unofficial Bitwarden-WebVault compatible with Vaultwarden
Url:        https://github.com/dani-garcia/bw_web_builds
Group:      Applications/System
BuildArch:  noarch
Source0:    bw_web_v%{version}.tar.gz

BuildRequires: tar

Requires: %{pkg_name} >= 1.26.0

BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-root

%description
%{SUMMARY}

%prep
%{__tar} -xf %{SOURCE0}

%clean

%build

%install
install -m 755 -d %{buildroot}%{_datarootdir}/%{pkg_name}

%{__cp} -dR web-vault %{buildroot}%{_datarootdir}/%{pkg_name}/

%files
%defattr(-,root,root,-)
%dir %attr(555,-,-) %{_datarootdir}/%{pkg_name}/
%{_datarootdir}/%{pkg_name}/*
%changelog
* Thu Oct 27 2022 Julian Röder <obs@masgalor.de>
- Update to version 2022.10.2
  * Bug fixes
* Fri Oct 21 2022 Julian Röder <obs@masgalor.de>
- Update to version 2022.10.1
  * Hide DuckDuckGo forwarding service by @stefan0xC in #89
  * Bug fixes
* Mon Oct 17 2022 Julian Röder <obs@masgalor.de>
- Update to version 2022.10.0
  * Added DuckDuckGo to forwarded email providers list
  * Created new flow for combined account/organization creation to simplify trial registration
  * Added Fastmail to forwarded email alias providers
  * Improvements to organization menu styles
  * Improvements to disabled organization display
  * The main Provider Portal screen now has at-a-glance seat and plan reporting for each client organization
  * Organizations will now have an event recorded in the event log when an owner or admin performs a vault export
  * Bug fix for “manage all collections” custom permissions
  * Bug fix for account referenceData not being populated
  * Bug fix for small typo in twoStepLogin modal (Community PR, thank you Patrick H. Lauke!)
  * Enable SCIM configuration
  * Bug fixes
* Thu Jul 28 2022 Julian Röder <obs@masgalor.de>
- Update to version 2022.6.2
  * Vault timeout fix that requires a minimum of 1 min lockout
  * Bug fixes for vault filters
  * Bug fixes
* Thu May 12 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.28.1
  * Bugfixes
* Mon Apr 25 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.28.0
  * Expansion of the generator tool to create unique usernames. Username types include plus addressed emails, catch-all emails, and random words.
  * Moved reports to top navigation and added new icons for vault health reports
  * Accessibility update on “Generator” to announce slider element when clicked with assistive technologies
  * Fixed an import issue of URLs and notes in the macOS and Safari importer
  * Bug fixes
* Mon Mar 28 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.27.0
  * Support for Dashlane, 1Password, and Myki importers
  * Improvements to SSO configuration
  * Introduce captcha upon 5 failed login attempts
  * Bug fixes
* Mon Mar 21 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.26.1
  * Icon updates
  * Light and dark theme fixes for WebAuthn and SSO
  * [Community] Display brand logo icons on credit card vault items
  * [Community] Updated inactive 2FA report to use 2fa.directory API v3
  * Stability, security and usability updates
  * Various bug fixes
* Mon Jan 31 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.25.1b
  * Unhide the API Key section under My Account by @jjlin in #59
* Mon Jan 24 2022 Julian Röder <obs@masgalor.de>
- Update to version 2.25.1
  * Bugfixes
* Tue Dec 14 2021 Julian Röder <obs@masgalor.de>
- Update to version 2.25.0
  * MacOS and Safari Importer
  * New LinkedField Custom Field Type
  * Key Connector for SSO with Customer Managed Encryption
  * Security & Bug Fixes
* Thu Oct 28 2021 Julian Röder <obs@masgalor.de>
- Update to version 2.24.1
  * Vault Timeout Policy
  * Disable Personal Vault Export Policy
  * Custom Role - Improved Collection Permissions
  * Admin Password Reset - Update Password after Reset
  * Auto-scale Organization Seats
  * Deprecate Business Portal
  * Web Vault Dark Mode
  * Accessibility and Usability Improvements
  * Bug Fixes
* Thu Oct 21 2021 Julian Röder <obs@masgalor.de>
- Update to version 2.23.0c
  * Require Enrollment Enterprise Policy for Admin Password Reset
  * CAPTCHA Support
  * Feedback - Add reveal-password button to the re-prompt modal
  * Bug fixes
  * Don't hide single organization policy
* Mon Sep 20 2021 Julian Röder <obs@masgalor.de>
- Update to version 2.22.3
  * New MSP/MSSP Provider Portal
  * Rename "Share" to "Move to Organization"
  * Support for Emoji's in Avatar
  * Added support for the Kannada language
  * Added support for the Azerbaijani language
  * Performance improvements for large vaults
  * Various bug fixes
* Tue Jul 27 2021 Julian Röder <obs@masgalor.de>
- Fix build errors on debian based distributions.
  * The instructions to download the sources were changed.
* Tue Jul 27 2021 Julian Röder <obs@masgalor.de>
- Update to version 2.21.1
  * Bug Fixes
  * Admin master password reset
  * Master password reprompt
  * Export/print events and audit report
  * Bulk remove, confirm, re-invite users for org
  * Bug and accessibility fixes
* Thu Jul  1 2021 Julian Röder <obs@masgalor.de>
- From now on, the webvault will be packaged from the corresponding git repository
  * This includes the versioning
- Update to version 2.20.4b
  * Removed the terms of service agreements at signup that aren't applicable to self hosted instances
  * WebAuthn bug fixes
  * WebAuthn fixes for some international locales
* Fri Apr 30 2021 Julian Röder <obs@masgalor.de>
- Project renamed to Vaultwarden
- Update to version 1.21.0

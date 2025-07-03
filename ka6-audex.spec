#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		audex
Summary:	An audio grabber tool for CD-ROM drives
Name:		ka6-%{kaname}
Version:	25.04.3
Release:	1
License:	GPL v2+/LGPL v2.1+/BSD-3-Clause/CC0-1.0/MIT
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	6243ec1edf82105889c4074aff441ff4
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 6.5
BuildRequires:	gettext-devel
BuildRequires:	ka6-libkcddb-devel >= 5.1
BuildRequires:	kf6-extra-cmake-modules >= 5.245.0
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kcompletion-devel >= 6.5.0
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kcoreaddons-devel >= 6.5.0
BuildRequires:	kf6-kcrash-devel
BuildRequires:	kf6-ki18n-devel >= 6.5.0
BuildRequires:	kf6-kiconthemes-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-ktextwidgets-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	libcdio-devel
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Audex is an audio grabber tool for CD-ROM drives built with KDE
Frameworks.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
rm -rf $RPM_BUILD_ROOT%{_localedir}/ie
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/audex
%{_desktopdir}/org.kde.audex.desktop
%dir %{_datadir}/audex
%dir %{_datadir}/audex/images
%{_datadir}/audex/images/cdcase_wo_latches.png
%{_datadir}/audex/images/latches.png
%{_iconsdir}/hicolor/scalable/apps/org.kde.audex.svg
%{_datadir}/metainfo/org.kde.audex.appdata.xml
%{_datadir}/solid/actions/audex-rip-audiocd.desktop

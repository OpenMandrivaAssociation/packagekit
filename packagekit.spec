%define major 4
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary:	A DBUS packaging abstraction layer
Name:	  	packagekit
Version:	0.3.1
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Configuration/Packaging
Source0: 	http://www.packagekit.org/releases/PackageKit-%version.tar.gz
URL:		http://www.packagekit.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:	dbus-glib-devel
BuildRequires:	sqlite3-devel
BuildRequires:	intltool
BuildRequires:	polkit-devel
BuildRequires:	docbook-utils
BuildRequires:	libxslt-proc
BuildRequires:	xmlto

%description
PackageKit is a DBUS abstraction layer that allows the session user to manage
packages in a secure way using a cross-distro, cross-architecture API.

%package -n %{libname}
Summary: Libraries for accessing PackageKit
Group: System/Configuration/Packaging

%description -n %{libname}
Libraries for accessing PackageKit.

%package -n %{develname}
Summary: Libraries and headers for PackageKit
Group: Development/Other
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Headers and libraries for PackageKit.

%package -n udev-packagekit
Summary: Tell PackageKit to install firmware that udev requires
Group: System/Configuration/Packaging
Requires: udev
Requires: %{name} = %{version}-%{release}

%description -n udev-packagekit
udev-packagekit tells PackageKit that firmware was not available and was
needed. This allows PackageKit to do the right thing and prompt for
the firmware to be installed.

%package cron
Summary: Cron job and related utilities for PackageKit
Group: System/Configuration/Packaging
Requires: crontabs
Requires: %{name} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%prep
%setup -q -n PackageKit-%version

%build
%configure2_5x --disable-static \
	--disable-alpm --disable-apt --disable-box --disable-conary \
	--enable-dummy --disable-opkg --disable-pisi --disable-poldek \
	--enable-smart --enable-urpmi --disable-yum --disable-yum2 --disable-zypp \
	--with-default-backend=urpmi
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%{find_lang} PackageKit

%clean
rm -rf $RPM_BUILD_ROOT

%files -f PackageKit.lang
%defattr(-, root, root)
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%{_sysconfdir}/bash_completion.d/*
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_bindir}/*
%{_datadir}/PackageKit
%{_datadir}/PolicyKit/policy/*.policy
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/mime/packages/*.xml
%{python_sitelib}/packagekit
%{_sbindir}/packagekitd
%dir %{_libdir}/packagekit-backend
%{_libdir}/packagekit-backend/*.so
%{_libexecdir}/pk-*
%{_mandir}/man1/*
%{_libdir}/pm-utils/sleep.d/95packagekit
%{_libexecdir}/PackageKitDbusTest.py
%ghost %verify(not md5 size mtime) %{_var}/lib/PackageKit/transactions.db
%ghost %verify(not md5 size mtime) %{_var}/run/PackageKit/job_count.dat

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/packagekit*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/packagekit-backend/*.la
%{_libdir}/pkgconfig/*.pc

%files -n udev-packagekit
%defattr(-, root, root)
%{_sysconfdir}/udev/rules.d/*.rules
/lib/udev/*.sh

%files cron
%defattr(-,root,root,-)
%config %{_sysconfdir}/cron.daily/*.cron
%config %{_sysconfdir}/sysconfig/packagekit-background
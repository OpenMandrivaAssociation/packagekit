%define major 14
%define libname %mklibname %name-glib %major
%define qtlib %mklibname %name-qt %major
%define develname %mklibname -d %name

Summary:	A DBUS packaging abstraction layer
Name:	  	packagekit
Version:	0.6.2
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Configuration/Packaging
Source0: 	http://www.packagekit.org/releases/PackageKit-%version.tar.bz2
Patch1:		packagekit-0.3.6-customize-vendor.patch
Patch3:		packagekit-0.6.1-link.patch
URL:		http://www.packagekit.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
BuildRequires:	dbus-glib-devel
BuildRequires:	libarchive-devel
BuildRequires:	sqlite3-devel
BuildRequires:	intltool
BuildRequires:	polkit-1-devel >= 0.92
BuildRequires:	docbook-utils
BuildRequires:	libxslt-proc
BuildRequires:	xmlto
BuildRequires:	qt4-devel
BuildRequires:	cppunit-devel
BuildRequires:	gtk+2-devel
BuildRequires:	pm-utils-devel
BuildRequires:	libgudev-devel
BuildRequires:	xulrunner-devel >= 1.9.1
BuildRequires:	gtk-doc
Suggests:	%{name}-gtk-module = %{version}
Suggests:	packagekit-gui
Obsoletes: udev-packagekit < %{version}-%{release}

%description
PackageKit is a DBUS abstraction layer that allows the session user to manage
packages in a secure way using a cross-distro, cross-architecture API.

%package -n %{libname}
Summary: Libraries for accessing PackageKit
Group: System/Configuration/Packaging

%description -n %{libname}
Libraries for accessing PackageKit.

%package -n %{qtlib}
Summary: QT libraries for accessing PackageKit
Group: System/Configuration/Packaging
Requires: %{name} = %{version}-%{release}

%description -n %{qtlib}
QT libraries for accessing PackageKit.

%package -n %{develname}
Summary: Libraries and headers for PackageKit
Group: Development/Other
Requires: %{libname} = %{version}-%{release}
Requires: %{qtlib} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: packagekit-qt-devel < %{version}

%description -n %{develname}
Headers and libraries for PackageKit.

%package cron
Summary: Cron job and related utilities for PackageKit
Group: System/Configuration/Packaging
Requires: crontabs
Requires: %{name} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%package browser-plugin
Summary: Browser Plugin for PackageKit
Group: System/Configuration/Packaging

%description browser-plugin
The PackageKit browser plugin allows web sites to offer the ability to
users to install and update packages from configured repositories
using PackageKit.

%package command-not-found
Summary: Ask the user to install command line programs automatically
Group: System/Configuration/Packaging

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%package gtk-module
Summary: Install fonts automatically using PackageKit
Group: System/Configuration/Packaging
Requires: pango

%description gtk-module
The PackageKit GTK+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%prep
%setup -q -n PackageKit-%version
%patch1 -p0
#%patch3 -p0

%build
%configure2_5x --disable-static --disable-gstreamer-plugin \
	--disable-alpm --disable-apt --disable-box --disable-conary \
	--enable-dummy --disable-opkg --disable-pisi --disable-poldek \
	--enable-smart --enable-urpmi --disable-yum --disable-zypp \
	--disable-ruck --with-default-backend=urpmi
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find %{buildroot} -name *.la | xargs rm

%{find_lang} PackageKit

%clean
rm -rf $RPM_BUILD_ROOT

%post
# the job count used to live in /var/run, but it's now in /var/lib with the
# other persistent bits
if [ -e %{_localstatedir}/run/PackageKit/job_count.dat ]; then
	mv %{_localstatedir}/run/PackageKit/job_count.dat %{_localstatedir}/lib/PackageKit/job_count.dat
fi

%files -f PackageKit.lang
%defattr(-, root, root)
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf
%{_sysconfdir}/bash_completion.d/*
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_bindir}/*
%{_datadir}/PackageKit
%{_datadir}/polkit-1/actions/*.policy
%{_libdir}/polkit-1/extensions/libpackagekit-action-lookup.so
%{_libdir}/pm-utils/sleep.d/95packagekit
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/mime/packages/*.xml
%{python_sitelib}/packagekit
%{_sbindir}/packagekitd
%{_sbindir}/pk-device-rebind
%dir %{_libdir}/packagekit-backend
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_smart.so
%{_libdir}/packagekit-backend/libpk_backend_test_fail.so
%{_libdir}/packagekit-backend/libpk_backend_test_nop.so
%{_libdir}/packagekit-backend/libpk_backend_test_spawn.so
%{_libdir}/packagekit-backend/libpk_backend_test_succeed.so
%{_libdir}/packagekit-backend/libpk_backend_test_thread.so
%{_libdir}/packagekit-backend/libpk_backend_urpmi.so
%{_mandir}/man1/*
%ghost %verify(not md5 size mtime) %{_var}/lib/PackageKit/transactions.db

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*packagekit-glib*.so.%{major}*
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir

%files -n %{qtlib}
%defattr(-, root, root)
%{_libdir}/*packagekit-qt*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%{_includedir}/PackageKit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/Modules/*.cmake

%files cron
%defattr(-,root,root,-)
%config %{_sysconfdir}/cron.daily/*.cron
%config %{_sysconfdir}/sysconfig/packagekit-background

%files browser-plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/packagekit-plugin.*

%files command-not-found
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found

%files gtk-module
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/modules/*.so

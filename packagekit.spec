%define _disable_ld_no_undefined 1
%define gstapi 1.0

%define major 18
%define gimajor 1.0
%define libname %mklibname %{name}-glib2_ %{major}
%define girname %mklibname packagekitglib-gir %{gimajor}
%define devname %mklibname %{name} -d

Summary:	A DBUS packaging abstraction layer
Name:		packagekit
Version:	1.1.7
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://www.packagekit.org
Source0:	http://www.freedesktop.org/software/PackageKit/releases/PackageKit-%{version}.tar.xz
Patch0:		packagekit-0.3.6-customize-vendor.patch
Patch1:		PackageKit-1.0.5-OpenMandriva-support.patch
# fix dispatcher hanging due to incorrect syntax
Patch2:		PackageKit-1.1.0-urpmi-dispatcher_fix.patch
# add missing summary and fix size reported as 0
Patch3:		PackageKit-1.1.0-urpmi_fixes.patch
# armv7 compiler bug here i think
Patch4:		autoptr-remove.patch

# Hif backend for OpenMandriva (DO NOT TOUCH NUMBERING!)
Patch1001:	1001-Revert-Remove-the-hif-backend.patch
Patch1002:	1002-Revert-Automatically-use-the-dnf-backend-instead-of-.patch
Patch1003:	1003-hif-Add-OpenMandriva-vendor.patch

BuildRequires:	autoconf
BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	docbook-style-xsl
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-base-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{gstapi})
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libhif)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(npapi-sdk)
BuildRequires:	pkgconfig(NetworkManager)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(xt)

Obsoletes:	%{name}-browser-plugin < 1.1.0-1
Provides:	%{name}-browser-plugin = 1.1.0-1

%description
PackageKit is a DBUS abstraction layer that allows the session user to manage
packages in a secure way using a cross-distro, cross-architecture API.

%files -f PackageKit.lang
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_bindir}/*
%{_datadir}/bash-completion/completions/pkcon
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/PackageKit
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.packagekit.rules
%{_libexecdir}/packagekitd
%{_libexecdir}/packagekit-direct
%{_libexecdir}/pk-offline-update
%dir %{_libdir}/packagekit-backend
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_test_fail.so
%{_libdir}/packagekit-backend/libpk_backend_test_nop.so
%{_libdir}/packagekit-backend/libpk_backend_test_spawn.so
%{_libdir}/packagekit-backend/libpk_backend_test_succeed.so
%{_libdir}/packagekit-backend/libpk_backend_test_thread.so
%{_libdir}/packagekit-backend/libpk_backend_hif.so
%{_libdir}/packagekit-backend/libpk_backend_urpmi.so
%{_mandir}/man1/*
%{_unitdir}/packagekit.service
%{_unitdir}/packagekit-offline-update.service
%{_unitdir}/system-update.target.wants
%dir %{_var}/lib/PackageKit
%ghost %verify(not md5 size mtime) %{_var}/lib/PackageKit/transactions.db
%dir %{_var}/cache/PackageKit
%dir %{_var}/cache/PackageKit/downloads

%post
# the job count used to live in /var/run, but it's now in /var/lib with the
# other persistent bits
if [ -e %{_localstatedir}/run/PackageKit/job_count.dat ]; then
    mv %{_localstatedir}/run/PackageKit/job_count.dat %{_localstatedir}/lib/PackageKit/job_count.dat
fi

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for accessing PackageKit
Group:		System/Configuration/Packaging
Obsoletes:	%{_lib}packagekit-glib16 < 0.8.11-5

%description -n %{libname}
Libraries for accessing PackageKit.

%files -n %{libname}
%{_libdir}/libpackagekit-glib2.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface library for %{name} glib
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface library for %{name} glib.

%files -n %{girname}
%{_libdir}/girepository-1.0/PackageKitGlib-%{gimajor}.typelib

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Libraries and headers for PackageKit
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Headers and libraries for PackageKit.

%files -n %{devname}
%{_includedir}/PackageKit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/PackageKitGlib-%{gimajor}.gir

#----------------------------------------------------------------------------

%package cron
Summary:	Cron job and related utilities for PackageKit
Group:		System/Configuration/Packaging
Requires:	%{name} = %{EVRD}
Requires:	crontabs

%description cron
Crontab and utilities for running PackageKit as a cron job.

%files cron
%config %{_sysconfdir}/cron.daily/*.cron
%config %{_sysconfdir}/sysconfig/packagekit-background

#----------------------------------------------------------------------------

%package gstreamer-plugin
Summary:	Install GStreamer codecs using PackageKit
Group:		System/Configuration/Packaging
Requires:	gstreamer%{gstapi}-tools
Requires:	%{name} = %{EVRD}
Requires(post,postun):	update-alternatives
Provides:	gst-install-plugins-helper

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%files gstreamer-plugin
%{_libexecdir}/pk-gstreamer-install

%post gstreamer-plugin
update-alternatives --install %{_libexecdir}/gst-install-plugins-helper gst-install-plugins-helper %{_libexecdir}/pk-gstreamer-install 10

%postun gstreamer-plugin
if [ "$1" = "0" ]; then
    if ! [ -e %{_libexecdir}/pk-gstreamer-install ]; then
        update-alternatives --remove gst-install-plugins-helper %{_libexecdir}/pk-gstreamer-install
    fi
fi

#----------------------------------------------------------------------------

%package command-not-found
Summary:	Ask the user to install command line programs automatically
Group:		System/Configuration/Packaging
Requires:	%{name} = %{EVRD}

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%files command-not-found
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found

#----------------------------------------------------------------------------

%package gtk2-module
Summary:	Install fonts automatically using PackageKit
Group:		System/Configuration/Packaging
Requires:	%{name} = %{EVRD}
Requires:	pango

%description gtk2-module
The PackageKit GTK2+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%files gtk2-module
%{_libdir}/gtk-2.0/modules/libpk-gtk-module.so

#----------------------------------------------------------------------------

%package gtk3-module
Summary:	Install fonts automatically using PackageKit
Group:		System/Configuration/Packaging
Requires:	%{name} = %{EVRD}
Requires:	pango

%description gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%files gtk3-module
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop
%{_libdir}/gtk-3.0/modules/libpk-gtk-module.so

#----------------------------------------------------------------------------

%prep
%setup -qn PackageKit-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch %arm
%patch4 -p1
%endif

%patch1001 -p1
%patch1002 -p1
%patch1003 -p1

# (tpg) ugly workaround !
# we have polkit 0.113 patched with few cherry-picks form upstream
# so it is safe to call that 0.113 is a 0.114 here
sed -i -e 's/polkit-gobject-1 >= 0.114/polkit-gobject-1 >= 0.113/' configure*


%build
%configure \
	--disable-static \
	--enable-vala=no \
	--enable-systemd \
	--enable-offline-update \
	--enable-bash-completion \
	--enable-local \
	--enable-gstreamer-plugin \
	--enable-command-not-found \
	--enable-urpmi \
	--enable-cron \
	--disable-alpm \
	--disable-aptcc \
	--disable-entropy \
	--disable-dnf \
	--enable-dummy \
	--enable-hif \
	--with-hif-vendor=openmandriva \
	--disable-pisi \
	--disable-poldek \
	--disable-portage \
	--disable-ports \
	--disable-katja \
	--enable-introspection \
	--disable-yum \
	--disable-zypp \
	--disable-nix \
	--with-systemdsystemunitdir=%{_systemunitdir} \
	--enable-python3

%make

%install
%makeinstall_std
%find_lang PackageKit

chmod -x %{buildroot}%{_sysconfdir}/cron.daily/*.cron
chmod o+r %{buildroot}%{_var}/lib/PackageKit/transactions.db

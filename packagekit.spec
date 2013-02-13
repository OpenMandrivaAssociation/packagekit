%define	major	16

%define girmajor 1.0
%define girname_plugin %mklibname packagekitplugin-gir %{girmajor}
%define girname_glib %mklibname packagekitglib-gir %{girmajor}

%define	libname %mklibname %{name}-glib2_ %{major}
%define oldlibname %mklibname %{name}-glib %{major}
%define	devname	%mklibname -d %{name}
%define _disable_ld_no_undefined 1

Summary:	A DBUS packaging abstraction layer
Name:		packagekit
Version:	0.8.7
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
URL:		http://www.packagekit.org
Source0:	http://www.packagekit.org/releases/PackageKit-%version.tar.xz
Patch1:		packagekit-0.3.6-customize-vendor.patch
Patch4:		PackageKit-0.6.14-libexecdir.patch
Patch6:		enable.diff

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gio-2.0) >= 2.16.1
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.16.1
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10)
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.14.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(mozilla-plugin) >= 8.0
BuildRequires:	pkgconfig(NetworkManager) >= 0.6.4
BuildRequires:	pkgconfig(nspr) >= 4.8
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(pm-utils)
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.98
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(xt)
BuildRequires:	intltool
BuildRequires:	gtk-doc

# fonts package in Mandriva do not have needed provides yet to be useful
Suggests:	%{name}-gtk3-module = %{version}
Suggests:	packagekit-gui
# No gtk2 plugin anymore
Obsoletes:	packagekit-gtk-module

%description
PackageKit is a DBUS abstraction layer that allows the session user to manage
packages in a secure way using a cross-distro, cross-architecture API.

%package -n	%{libname}
Obsoletes:	%{oldlibname}
Summary:	Libraries for accessing PackageKit
Group:		System/Configuration/Packaging

%description -n	%{libname}
Libraries for accessing PackageKit.

%package -n	%{girname_plugin}
Summary:	GObject Introspection interface library for %{name} plugin
Group:		System/Libraries

%description -n	%{girname_plugin}
GObject Introspection interface library for %{name} plugin.

%package -n	%{girname_glib}
Summary:	GObject Introspection interface library for %{name} glib
Group:		System/Libraries

%description -n	%{girname_glib}
GObject Introspection interface library for %{name} glib.

%package -n	%{devname}
Summary:	Libraries and headers for PackageKit
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname_glib} = %{version}-%{release}
Requires:	%{girname_plugin} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	packagekit-qt-devel < %{version}

%description -n	%{devname}
Headers and libraries for PackageKit.

%package	cron
Summary:	Cron job and related utilities for PackageKit
Group:		System/Configuration/Packaging
Requires:	crontabs
Requires:	%{name} = %{version}-%{release}

%description	cron
Crontab and utilities for running PackageKit as a cron job.

%package	gstreamer-plugin
Summary:	Install GStreamer codecs using PackageKit
Group:		System/Configuration/Packaging
Requires:	gstreamer-tools
Requires:	%{name} = %{version}-%{release}
Requires(post):	update-alternatives
Requires(postun):update-alternatives
Provides:	gst-install-plugins-helper

%description	gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%package	browser-plugin
Summary:	Browser Plugin for PackageKit
Group:		System/Configuration/Packaging
Requires:	%{name} = %{version}-%{release}

%description	browser-plugin
The PackageKit browser plugin allows web sites to offer the ability to
users to install and update packages from configured repositories
using PackageKit.

%package	command-not-found
Summary:	Ask the user to install command line programs automatically
Group:		System/Configuration/Packaging
Requires:	%{name} = %{version}-%{release}

%description	command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%package	gtk3-module
Summary:	Install fonts automatically using PackageKit
Group:		System/Configuration/Packaging
Requires:	pango
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}packagekit-glib14 < 0.7.4-2

%description	gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%package        gtk2-module
Summary:        Install fonts automatically using PackageKit
Group:          System/Configuration/Packaging
Requires:       pango
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{_lib}packagekit-glib14 < 0.7.4-2

%description    gtk2-module
The PackageKit GTK+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%prep
%setup -q -n PackageKit-%{version}
%patch1 -p0
%patch4 -p0 -b .libexec~
%patch6 -p1 -b .enable~

%build
%configure2_5x	\
	--disable-static \
	--enable-gstreamer-plugin \
	--disable-alpm \
	--disable-apt \
	--disable-box \
	--disable-conary \
	--enable-dummy \
	--disable-opkg \
	--disable-pisi \
	--disable-poldek \
	--enable-smart \
	--enable-urpmi \
	--enable-introspection \
	--disable-yum \
	--disable-zypp \
	--with-default-backend=urpmi

%make

%install
%makeinstall_std

find %{buildroot} -name *.la | xargs rm

%{find_lang} PackageKit

chmod -x %{buildroot}/%{_sysconfdir}/cron.daily/*.cron
chmod o+r %{buildroot}/%{_var}/lib/PackageKit/transactions.db

%post
# the job count used to live in /var/run, but it's now in /var/lib with the
# other persistent bits
if [ -e %{_localstatedir}/run/PackageKit/job_count.dat ]; then
	mv %{_localstatedir}/run/PackageKit/job_count.dat %{_localstatedir}/lib/PackageKit/job_count.dat
fi

%post gstreamer-plugin
update-alternatives --install %{_libexecdir}/gst-install-plugins-helper gst-install-plugins-helper %{_libexecdir}/pk-gstreamer-install 10

%postun gstreamer-plugin
if [ "$1" = "0" ]; then
    if ! [ -e %{_libexecdir}/pk-gstreamer-install ]; then
        update-alternatives --remove gst-install-plugins-helper %{_libexecdir}/pk-gstreamer-install
    fi
fi

%files -f PackageKit.lang
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf
%dir %{_sysconfdir}/PackageKit/events
%dir %{_sysconfdir}/PackageKit/events/post-transaction.d
%{_sysconfdir}/PackageKit/events/post-transaction.d/README
%dir %{_sysconfdir}/PackageKit/events/pre-transaction.d
%{_sysconfdir}/PackageKit/events/pre-transaction.d/README
%{_sysconfdir}/bash_completion.d/*
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_unitdir}/packagekit-offline-update.service
%{_bindir}/*
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/mime/packages/*.xml
%{_sbindir}/pk-device-rebind
%{_datadir}/PackageKit
%{_datadir}/polkit-1/actions/*.policy
%{python_sitelib}/packagekit
%{_libexecdir}/packagekitd
%{_libexecdir}/pk-clear-offline-update
%{_libexecdir}/pk-offline-update
%{_libexecdir}/pk-trigger-offline-update
%{_libexecdir}/pm-utils/sleep.d/95packagekit
%dir %{_libdir}/packagekit-backend
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_smart.so
%{_libdir}/packagekit-backend/libpk_backend_test_fail.so
%{_libdir}/packagekit-backend/libpk_backend_test_nop.so
%{_libdir}/packagekit-backend/libpk_backend_test_spawn.so
%{_libdir}/packagekit-backend/libpk_backend_test_succeed.so
%{_libdir}/packagekit-backend/libpk_backend_test_thread.so
%{_libdir}/packagekit-backend/libpk_backend_urpmi.so
%{_libdir}/packagekit-plugins/*.so
%{_mandir}/man1/*
%dir %{_var}/lib/PackageKit
%ghost %verify(not md5 size mtime) %{_var}/lib/PackageKit/transactions.db
%dir %{_var}/cache/PackageKit
%dir %{_var}/cache/PackageKit/downloads

%files -n %{libname}
%{_libdir}/*packagekit-glib*.so.%{major}*

%files -n %{girname_plugin}
%{_libdir}/girepository-1.0/PackageKitPlugin-1.0.typelib

%files -n %{girname_glib}
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files -n %{devname}
%{_includedir}/PackageKit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gir-1.0/PackageKitPlugin-1.0.gir

%files cron
%config %{_sysconfdir}/cron.daily/*.cron
%config %{_sysconfdir}/sysconfig/packagekit-background

%files gstreamer-plugin
%{_libexecdir}/pk-gstreamer-install

%files browser-plugin
%{_libdir}/mozilla/plugins/packagekit-plugin.*

%files command-not-found
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found

%files gtk3-module
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop
%{_libdir}/gtk-3.0/modules/libpk-gtk-module.so

%files gtk2-module
%{_libdir}/gtk-2.0/modules/libpk-gtk-module.so

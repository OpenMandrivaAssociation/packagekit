%define _disable_ld_no_undefined 1
%define gstapi 1.0

%define major 18
%define gimajor 1.0
%define libname %mklibname %{name}-glib2_ %{major}
%define girname %mklibname packagekitglib-gir %{gimajor}
%define devname %mklibname %{name} -d

# For libdnf minimal enforced dep
%global min_ldnf_ver 0.43.1
%global min_ldnf_verrel %{min_ldnf_ver}-1
%global ldnfsomajor 2

Summary:	A DBUS packaging abstraction layer
Name:		packagekit
Version:	1.2.0
Release:	1
License:	GPLv2+
Group:		System/Configuration/Packaging
Url:		http://www.packagekit.org
Source0:	http://www.freedesktop.org/software/PackageKit/releases/PackageKit-%{version}.tar.xz
Patch0:		packagekit-0.3.6-customize-vendor.patch

BuildRequires:	meson
BuildRequires:	xsltproc
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(libdnf) >= %{min_ldnf_ver}
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
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(npapi-sdk)
BuildRequires:	pkgconfig(libnm)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(xt)
Requires(post):	rpm-helper
Obsoletes:	%{name}-browser-plugin < 1.1.0-1
Provides:	%{name}-browser-plugin = 1.1.0-1
# Obsolete Zypp backend
Obsoletes:	%{name}-backend-zypp < 1.1.12-6
Conflicts:	%{name}-backend-zypp < %{EVRD}
# Merge DNF backend package back into main package
Obsoletes:	%{name}-backend-dnf < 1.1.13
Provides:	%{name}-backend-dnf = %{EVRD}
Requires:	%{mklibname dnf %{ldnfsomajor}} >= %{min_ldnf_verrel}
Obsoletes:	%{name}-gtk2-module

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
%{_libdir}/packagekit-backend/libpk_backend_dnf.so
%{_libdir}/packagekit-backend/libpk_backend_test_fail.so
%{_libdir}/packagekit-backend/libpk_backend_test_nop.so
%{_libdir}/packagekit-backend/libpk_backend_test_spawn.so
%{_libdir}/packagekit-backend/libpk_backend_test_succeed.so
%{_libdir}/packagekit-backend/libpk_backend_test_thread.so
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

# Remove leftover symlinks from /etc/systemd; the offline update service is	
# instead now hooked into /usr/lib/systemd/system/system-update.target.wants	
systemctl disable packagekit-offline-update.service > /dev/null 2>&1 || :
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
Requires(post,postun):	rpm-helper
Requires(post,postun):	chkconfig
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
%autosetup -n PackageKit-%{version} -p1

%build
%meson \
        -Dgtk_doc=true \
	-Ddnf_vendor=openmandriva \
	-Dsystemd=true \
	-Dsystemdsystemunitdir=%{_unitdir} \
        -Dpython_backend=false \
        -Dpackaging_backend=dnf \
        -Dlocal_checkout=false
	
%meson_build

%install
%meson_install

# Create directories for downloaded appstream data	
mkdir -p %{buildroot}%{_localstatedir}/cache/app-info/{icons,xmls}	

# create a link that GStreamer will recognise	
cd %{buildroot}%{_libexecdir} > /dev/null
ln -s pk-gstreamer-install gst-install-plugins-helper	
cd -
	
# enable packagekit-offline-updates.service here for now
# https://github.com/hughsie/PackageKit/issues/401
# https://bugzilla.redhat.com/show_bug.cgi?id=1833176
mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants/	
ln -sf ../packagekit-offline-update.service %{buildroot}%{_unitdir}/system-update.target.wants/packagekit-offline-update.service

%find_lang PackageKit

chmod -x %{buildroot}%{_sysconfdir}/cron.daily/*.cron
chmod o+r %{buildroot}%{_var}/lib/PackageKit/transactions.db

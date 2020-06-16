%define api		0.1
%define major		1
%define libname		%mklibname ayatana-appindicator3_ %{major}
%define girayatananame	%mklibname ayatana-appindicator3-gir %{api}
%define develname	%mklibname ayatana-appindicator3 -d

%bcond_without mono

Name:		libayatana-appindicator
Version:	0.5.4
Release:	%mkrel 1
Summary:	Ayatana application indicators library
License:	LGPLv2 AND LGPLv3 AND GPLv3
Group:		System/Libraries
URL:		https://ayatanaindicators.github.io/
Source0:	https://github.com/AyatanaIndicators/libayatana-appindicator/archive/%{version}/%{name}-%{version}.tar.gz
# Don't add -Werror on build: the code is aging and does not keep up.
Patch0:		libayatanaappindicator-disable-werror.patch
# Fix location of .pc files.
Patch1:		libayatana-appindicator-fix-mono-dir.patch
# Python2 is EOL
Patch2:		libayatana-appindicator-drop-python2-code.patch
BuildRequires:	mate-common
BuildRequires:	vala
BuildRequires:	pkgconfig(ayatana-indicator3-0.4)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0)
%if %{with mono}
BuildRequires:	pkgconfig(gapi-2.0)
BuildRequires:	pkgconfig(gtk-sharp-2.0)
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(nunit)
%endif

%description
A library to allow applications to add an icon into the
StatusNotifier-compatible notification area. If none are available,
it also provides an XEmbed-tray fallback.

#------------------------------------------------

%package -n	%{libname}
Summary:	Ayatana application indicators library for GTK+3
Group:		System/Libraries

%description -n	%{libname}
A library to allow applications to add an icon into the
StatusNotifier-compatible notification area. If none are available,
it also provides an XEmbed-tray fallback.

This package contains the GTK+3 version of the library.

#------------------------------------------------

%package -n	%{girayatananame}
Summary:	GObject Introspection interface description for Ayatana Application Indicator3
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girayatananame}
This package contains the GObject Introspection interface description
for Ayatana Application Indicator3 and GTK+3.

#------------------------------------------------

%package -n	%{develname}
Summary:	Development package for %{name}3 (GTK+3)
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girayatananame} = %{version}-%{release}
Provides:	ayatana-appindicator3-devel = %{version}-%{release}

%description -n	%{develname}
Header files for development with %{name}3 (GTK+3).

#------------------------------------------------

%package	doc
Summary:	Documentation for libayatana-appindicator3
Group:		Documentation
BuildArch:	noarch

%description	doc
This package contains the documentation for the Ayatana
appindicator3 libraries.

#------------------------------------------------

%if %{with mono}
%package -n	ayatana-appindicator-sharp
Summary:	Ayatana application indicators library for C#
Group:		Development/C#

%description -n	ayatana-appindicator-sharp
This package provides the ayatana-appindicator-sharp assembly that
allows CLI (.NET) applications to take menus from applications and
place them in the panel.

This package provides assemblies to be used by applications.

#------------------------------------------------

%package -n	ayatana-appindicator-sharp-devel
Summary:	Development files for ayatana-appindicator-sharp
Group:		Development/C#
Requires:	ayatana-appindicator-sharp >= %{version}-%{release}

%description -n	ayatana-appindicator-sharp-devel
This package contains the development files for the
ayatana-appindicator-sharp library.
%endif

#------------------------------------------------

%prep
%autosetup -p1

%build
NOCONFIGURE=1 ./autogen.sh

%if %{with mono}
export CSC=%{_bindir}/mcs
%endif

%configure \
	--disable-static  \
	--enable-gtk-doc   \
	--disable-mono-test \
	--with-gtk=3
%__make

%install
%make_install

find %{buildroot} -name '*.la' -delete

%files -n %{libname}
%license COPYING*
%doc README
%{_libdir}/libayatana-appindicator3.so.%{major}{,.*}

%files -n %{girayatananame}
%license COPYING*
%doc README
%{_libdir}/girepository-1.0/AyatanaAppIndicator3-%{api}.typelib

%files -n %{develname}
%license COPYING*
%doc README
%{_includedir}/libayatana-appindicator3-%{api}/
%{_libdir}/libayatana-appindicator3.so
%{_libdir}/pkgconfig/ayatana-appindicator3-%{api}.pc
%{_datadir}/gir-1.0/AyatanaAppIndicator3-%{api}.gir
%{_datadir}/vala/vapi/ayatana-appindicator3-%{api}.*

%files doc
%{_datadir}/gtk-doc/html/%{name}/

%if %{with mono}
%files -n ayatana-appindicator-sharp
%license COPYING*
%doc README
%{_libdir}/ayatana-appindicator-sharp-%{api}/
%{_prefix}/lib/mono/ayatana-appindicator-sharp/
%{_prefix}/lib/mono/gac/ayatana-appindicator-sharp/
%{_prefix}/lib/mono/gac/policy.0.0.ayatana-appindicator-sharp/

%files -n ayatana-appindicator-sharp-devel
%license COPYING*
%doc README
%{_libdir}/pkgconfig/ayatana-appindicator-sharp-%{api}.pc
%endif

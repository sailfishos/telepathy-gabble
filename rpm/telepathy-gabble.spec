Name:       telepathy-gabble
Summary:    A Jabber/XMPP connection manager
Version:    0.18.4
Release:    1
License:    LGPLv2+
URL:        https://telepathy.freedesktop.org/
Source0:    %{name}-%{version}.tar.bz2
Source1:    mktests.sh
Source2:    INSIGNIFICANT
Patch0:     nemo-tests-dir-fix.patch
Patch1:     0001-Change-default-keepalive-interval-to-2.5-minutes.patch
Patch2:     0002-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
Patch3:     0001-xmpp-console-Explicitly-state-python-in-the-shebang.patch
Patch4:     telepathy-gabble-0.18.4-python3.patch
Patch5:     0001-convert-tests-to-python3.patch
Patch6:     wocky-Make-GTK-Docs-optional.patch
Patch7:     wocky-fix-mem-leak.patch
Patch8:     wocky-openssl-1.1-compat.patch
BuildRequires:  pkgconfig(dbus-1) >= 1.1.0
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(telepathy-glib) >= 0.19.9
BuildRequires:  pkgconfig(glib-2.0) >= 2.44
BuildRequires:  pkgconfig(gobject-2.0) >= 2.44
BuildRequires:  pkgconfig(gthread-2.0) >= 2.44
BuildRequires:  pkgconfig(gio-2.0) >= 2.44
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.32
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libsoup-2.4) >= 2.42
BuildRequires:  pkgconfig(nice) >= 0.0.11
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libiphb) >= 0.61.31
BuildRequires:  ca-certificates
BuildRequires:  python3-devel
BuildRequires:  python3-twisted
BuildRequires:  dbus-python3
Requires:       telepathy-mission-control >= 5.5.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Jabber/XMPP connection manager, that handles single and multi-user
chats and voice calls.


%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}

%description doc
Man pages and other documentation for %{name}.


%package tests
Summary:    Tests package for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   python3-twisted
Requires:   pyOpenSSL
Requires:   dbus-python3
Requires:   python3-gobject

%description tests
The %{name}-tests package contains tests and tests.xml for automated testing.


%prep
%setup -q -n %{name}-%{version}/%{name}

# nemo-tests-dir-fix.patch
%patch0 -p1
# 0001-Change-default-keepalive-interval-to-2.5-minutes.patch
%patch1 -p1
# 0002-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
%patch2 -p1
# 0001-xmpp-console-Explicitly-state-python-in-the-shebang.patch
%patch3 -p1
# telepathy-gabble-0.18.4-python3.patch
%patch4 -p1
# 0001-convert-tests-to-python3.patch
%patch5 -p1

%__cp %{SOURCE1} tests/
%__cp %{SOURCE2} tests/

cd lib/ext/wocky
%patch6 -p1
%patch7 -p1
# wocky-openssl-1.1-compat.patch  (for openssl compile errors)
%patch8 -p1

%build
%autogen --disable-submodules --no-configure
# launch Wocky's autogen.sh
cd lib/ext/wocky
%autogen --no-configure
cd ../../..

%configure --disable-static \
  --disable-gtk-doc \
  --enable-installed-tests \
  --enable-is-a-phone \
  --with-tls=openssl

%make_build

%install
%make_install

sh tests/mktests.sh > %{buildroot}/opt/tests/%{name}/tests.xml
install -m 0644 tests/INSIGNIFICANT %{buildroot}/opt/tests/%{name}/INSIGNIFICANT
install -m 0644 tests/README %{buildroot}/opt/tests/%{name}/README

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/%{name}-xmpp-console
%{_libexecdir}/%{name}
%dir %{_libdir}/telepathy/gabble-0
%dir %{_libdir}/telepathy/gabble-0/lib
%dir %{_libdir}/telepathy/gabble-0/plugins
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins-*.so
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins.so
%{_libdir}/telepathy/gabble-0/lib/libwocky-telepathy-gabble-*.so
%{_libdir}/telepathy/gabble-0/lib/libwocky.so
%{_libdir}/telepathy/gabble-0/plugins/libconsole.so
%{_libdir}/telepathy/gabble-0/plugins/libgateways.so
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/managers/*.manager

%files doc
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%{_docdir}/%{name}/
%{_mandir}/man8/%{name}.8.gz

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*

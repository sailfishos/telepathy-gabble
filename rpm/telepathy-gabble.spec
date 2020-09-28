Name:       telepathy-gabble

Summary:    A Jabber/XMPP connection manager
Version:    0.18.4
Release:    1
License:    LGPLv2+ and BSD
URL:        https://telepathy.freedesktop.org/
Source0:    %{name}-%{version}.tar.gz
Source1:    INSIGNIFICANT
Source2:    mktests.sh
Patch0:     nemo-tests-dir-fix.patch
Patch1:     0001-Disable-parallel-build-for-extensions-directory.patch
Patch2:     wocky-disable-gtkdoc.patch
Patch3:     wocky-mem-leak.patch
Patch4:     0001-Change-default-keepalive-interval-to-2.5-minutes.patch
Patch5:     0001-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
Patch6:     0001-xmpp-console-Explicitly-state-python-in-the-shebang.patch
Patch7:     telepathy-gabble-0.18.4-python3.patch
Patch8:     wocky-openssl-1.1-compat.patch
Patch9:     0001-convert-tests-to-python3.patch
Requires:   telepathy-mission-control
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-1) >= 1.1.0
BuildRequires:  pkgconfig(nice) >= 0.0.11
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(telepathy-glib) >= 0.19.9
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gobject-2.0) >= 2.32
BuildRequires:  pkgconfig(gthread-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-2.0) >= 2.32
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.32
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libidn)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libiphb)
BuildRequires:  python3-devel
BuildRequires:  ca-certificates
BuildRequires:  python3-twisted
BuildRequires:  dbus-python3

%description
A Jabber/XMPP connection manager, that handles single and multi-user
chats and voice calls.


%package doc
Summary:    Documentation for %{name}
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
The %{name}-tests package contains tests and
tests.xml for automated testing.


%prep
%setup -q -n %{name}-%{version}/%{name}

# nemo-tests-dir-fix.patch
%patch0 -p1
# 0001-Disable-parallel-build-for-extensions-directory.patch
%patch1 -p1
cd lib/ext/wocky
%patch2 -p1
%patch3 -p1
# wocky-openssl-1.1-compat.patch  (for openssl compile errors)
%patch8 -p1
cd ../../..
# 0001-Change-default-keepalive-interval-to-2.5-minutes.patch
%patch4 -p1
# 0001-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
%patch5 -p1
# 0001-xmpp-console-Explicitly-state-python-in-the-shebang.patch
%patch6 -p1
# telepathy-gabble-0.18.4-python3.patch
%patch7 -p1
# 0001-convert-tests-to-python3.patch
%patch9 -p1

%__cp $RPM_SOURCE_DIR/mktests.sh tests/
%__cp $RPM_SOURCE_DIR/INSIGNIFICANT tests/
%__chmod 0755 tests/mktests.sh
%__chmod 0644 tests/INSIGNIFICANT

%build
cd lib/ext/wocky
%autogen --no-configure --disable-gtk-doc
cd ../../..
%autogen --disable-submodules --no-configure

%reconfigure --disable-static \
    --enable-installed-tests

make %{_smp_mflags}

tests/mktests.sh > tests/tests.xml

%install
rm -rf %{buildroot}
%make_install

install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/tests.xml
install -m 0644 tests/INSIGNIFICANT $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/INSIGNIFICANT
install -m 0644 tests/README $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/README

install -m 0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}/ AUTHORS NEWS README

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_libexecdir}/%{name}
%{_bindir}/telepathy-gabble-xmpp-console
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
%doc %{_docdir}/%{name}/
%{_mandir}/man8/%{name}.8.gz

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*

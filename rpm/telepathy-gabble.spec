Name:       telepathy-gabble

Summary:    A Jabber/XMPP connection manager
Version:    0.18.3
Release:    1
Group:      Applications/Communications
License:    LGPLv2+ and BSD
URL:        http://telepathy.freedesktop.org/wiki/
Source0:    http://telepathy.freedesktop.org/releases/telepathy-gabble/%{name}-%{version}.tar.gz
Source1:    INSIGNIFICANT
Source2:    mktests.sh
Patch0:     nemo-tests-dir-fix.patch
Patch1:     0001-Disable-parallel-build-for-extensions-directory.patch
Patch2:	    wocky-disable-gtkdoc.patch
Patch3:     wocky-mem-leak.patch
Patch4:     0001-Change-default-keepalive-interval-to-2.5-minutes.patch
Patch5:     0001-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
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
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libiphb)
BuildRequires:  python
BuildRequires:  ca-certificates
BuildRequires:  python-twisted
BuildRequires:  dbus-python

%description
A Jabber/XMPP connection manager, that handles single and multi-user
chats and voice calls.


%package tests
Summary:    Tests package for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   python-twisted
Requires:   pyOpenSSL
Requires:   dbus-python
Requires:   pygobject2

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
cd ../../..
# 0001-Change-default-keepalive-interval-to-2.5-minutes.patch
%patch4 -p1
# 0001-switch-to-using-gireactor-to-work-with-new-gi-based-.patch
%patch5 -p1

# >> setup
%__cp $RPM_SOURCE_DIR/mktests.sh tests/
%__cp $RPM_SOURCE_DIR/INSIGNIFICANT tests/
%__chmod 0755 tests/mktests.sh
%__chmod 0644 tests/INSIGNIFICANT
# << setup

%build
# >> build pre
cd lib/ext/wocky
%autogen --no-configure --disable-gtk-doc
cd ../../..
%autogen --disable-submodules --no-configure
# << build pre

%reconfigure --disable-static \
    --enable-installed-tests

make %{?jobs:-j%jobs}

# >> build post
tests/mktests.sh > tests/tests.xml
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/tests.xml
install -m 0644 tests/INSIGNIFICANT $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/INSIGNIFICANT
install -m 0644 tests/README $RPM_BUILD_ROOT/opt/tests/telepathy-gabble/README
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%doc %{_datadir}/doc/%{name}/*.html
%{_libexecdir}/%{name}
%{_bindir}/telepathy-gabble-xmpp-console
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins-*.so
%{_libdir}/telepathy/gabble-0/lib/libgabble-plugins.so
%{_libdir}/telepathy/gabble-0/lib/libwocky-telepathy-gabble-*.so
%{_libdir}/telepathy/gabble-0/lib/libwocky.so
%{_libdir}/telepathy/gabble-0/plugins/libconsole.so
%{_libdir}/telepathy/gabble-0/plugins/libgateways.so
%{_datadir}/dbus-1/services/*.service
%{_datadir}/telepathy/managers/*.manager
%{_mandir}/man8/%{name}.8.gz
# << files

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*
# >> files tests
# << files tests

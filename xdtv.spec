#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	Video4Linux Stream Capture Viewer
Summary(pl.UTF-8):   Program do oglądania strumienia z Video4Linux
Name:		xdtv
Version:	2.3.3
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/xawdecode/%{name}-%{version}.tar.gz
# Source0-md5:	72528d2205ac5e22ae766283a993225c
Source1:	xawdecode.desktop
Patch0:		xawdecode-xvid.patch
Patch1:		%{name}-ffmpeg.patch
Patch2:		%{name}-parallel-install.patch
Patch3:		%{name}-setXid.patch
URL:		http://xawdecode.sourceforge.net/
#BuildRequires:	Mowitz-devel	-- would make sense with neXtaw instead of Xaw3d
BuildRequires:	XFree86-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.4.9
BuildRequires:	lame-libs-devel >= 3.96.1
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	xvid-devel >= 1:1.1.0
BuildRequires:	zvbi-devel >= 0.2.14
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/misc
Requires:	xvid >= 1:1.1.0
Requires:	zvbi >= 0.2.14
Provides:	xawdecode
Obsoletes:	xawdecode
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults

%description
X11 TV application based on xawtv 2.x series with plugin capabilities.

%description -l pl.UTF-8
Aplikacja TV dla X11 oparta na xawtv 2.x z możliwością używania
wtyczek.

%package devel
Summary:	Development files for xawdecode
Summary(pl.UTF-8):   Pliki do programowania z użyciem xawdecode
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	xawdecode-devel

%description devel
Development files for xawdecode.

%description devel -l pl.UTF-8
Pliki do programowania z użyciem xawdecode.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

rm -rf libavformat libavcodec libavutil libpostproc

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-cpu-detection \
	--disable-divx4linux \
	%{!?with_lirc:--disable-lirc} \
	%{?with_lirc:--enable-lirc} \
	--disable-mowitz \
	--enable-external-ffmpeg \
	--disable-nextaw \
	--disable-xaw95 \
	--disable-xawm \
	--with-x \
	--with-appdefaultsdir=%{_appdefsdir} \
	--with-fontdir=%{_fontsdir}/misc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	FONTDIR=%{_fontsdir}/misc

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc

%postun
fontpostinst misc

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQfr-xdtv
%doc lircrc.hauppauge.sample lircrc.miro.sample lisez-moi README*
%doc xdtvrc.sample
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdtv*
%attr(755,root,root) %{_bindir}/xdtv
%attr(755,root,root) %{_bindir}/xdtv_[a-uw]*
%attr(4755,root,root) %{_bindir}/xdtv_v4l-conf
%dir %{_datadir}/xdtv
%{_datadir}/xdtv/icons
%{_appdefsdir}/*
%{_mandir}/man1/*
%{_fontsdir}/misc/*.pcf.gz
%{_desktopdir}/%{name}.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/xdtv

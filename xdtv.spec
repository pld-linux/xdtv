#
# Conditional build:
%bcond_without	lirc	# without LIRC support
#
Summary:	Video4Linux Stream Capture Viewer
Summary(pl):	Program do ogl±dania strumienia z Video4Linux
Name:		xawdecode
Version:	2.0.1
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/xawdecode/xdtv-%{version}.tar.bz2
# Source0-md5:	8dcb3a814c8db47009ddbe03787eeb1c
Source1:	xawdecode.desktop
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-xvid.patch
Patch3:		%{name}-link.patch
URL:		http://xawdecode.sourceforge.net/
#BuildRequires:	Mowitz-devel	-- would make sense with neXtaw instead of Xaw3d
BuildRequires:	XFree86-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ffmpeg-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libjpeg-devel
%{?with_lirc:BuildRequires:	lirc-devel}
BuildRequires:	xvid-devel
BuildRequires:	zvbi-devel
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/misc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults

%description
X11 TV application based on xawtv 2.x series with plugin capabilities.

%description -l pl
Aplikacja TV dla X11 oparta na xawtv 2.x z mo¿liwo¶ci± u¿ywania
wtyczek.

%package devel
Summary:	Development files for xawdecode
Summary(pl):	Pliki do programowania z u¿yciem xawdecode
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for xawdecode.

%description devel -l pl
Pliki do programowania z u¿yciem xawdecode.

%prep
%setup -q -n xdtv-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-alsa \
	--disable-cpu-detection \
	--disable-divx4linux \
	%{!?with_lirc:--disable-lirc} \
	%{?with_lirc:--enable-lirc} \
	--disable-mowitz \
	--disable-nextaw \
	--disable-xaw95 \
	--disable-xawm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	FONTDIR=%{_fontsdir}/misc

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc

%postun
fontpostinst misc

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQfr-xdtv libavc-rate-control.txt
%doc lircrc.hauppauge.sample lircrc.miro.sample lisez-moi README*
%doc xdtvrc.sample
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xdtv*
%attr(755,root,root) %{_bindir}/xdtv
%attr(755,root,root) %{_bindir}/xdtv_[a-uw]*
%attr(4755,root,root) %{_bindir}/xdtv_v4l-conf
%dir %{_datadir}/xdtv
%{_datadir}/xdtv/icons
%{_appdefsdir}/*
%{_mandir}/man1/*
%{_fontsdir}/misc/*.pcf
%{_desktopdir}/%{name}.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/xdtv

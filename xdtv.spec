Name:		xawdecode
Summary:	Video4Linux Stream Capture Viewer
Version:	1.6.8
Release:	0.20030218.0
License:	GPL
URL:		http://xawdecode.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/xawdecode/%{name}-2003-02-18.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-xvid.patch
Group:		X11/Applications/Multimedia
Requires:	XFree86-libs
#Requires:	divx4linux
Requires:	ffmpeg
Requires:	lame-libs
Requires:	Xaw3d
Requires:	lirc
Requires:	libjpeg
BuildRequires:	XFree86-devel
#BuildRequires:	divx4linux-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	lame-libs-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	lirc-devel
BuildRequires:	libjpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
X11 TV application based on xawtv 2.x series with plugin capabilities

%package devel
Summary:	Developpement files for xawdecode
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Developpement files for xawdecode.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure --disable-divx4linux --disable-alsa
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	FONTDIR=%{_fontsdir}/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post
cd %{_fontsdir}/misc                                                            
umask 022                                                                       
%{_bindir}/mkfontdir                                                            
xset fp rehash >/dev/null 2>/dev/null || true

%postun
cd %{_fontsdir}/misc                                                            
umask 022                                                                       
%{_bindir}/mkfontdir                                                            
xset fp rehash >/dev/null 2>/dev/null || true

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQfr-xawdecode libavc-rate-control.txt
%doc lircrc.hauppauge.sample lircrc.miro.sample lisez-moi README*
%doc xawdecoderc.sample
/usr/X11R6/lib/X11/app-defaults/*
%attr(755,root,root) %{_bindir}/xawdecode
%attr(4755,root,root) %{_bindir}/v4l-conf
%{_mandir}/man1/*
%{_datadir}/%{name}/icons/*
%{_fontsdir}/misc/*.pcf

%files devel
%defattr(644,root,root,755)
%{_includedir}/*

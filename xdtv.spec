#
# Conditional build:
# --without lirc
#
Summary:	Video4Linux Stream Capture Viewer
Summary(pl):	Program do ogl±dania strumienia z Video4Linux
Name:		xawdecode
Version:	1.6.8
Release:	0.20030218.0
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/xawdecode/%{name}-2003-02-18.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-xvid.patch
URL:		http://xawdecode.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	divx4linux-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libjpeg-devel
%{!?_without_lirc:BuildRequires:	lirc-devel}
BuildRequires:	xvid-devel
Requires:	XFree86-libs
Requires:	Xaw3d
#Requires:	divx4linux
Requires:	ffmpeg
Requires:	lame-libs
Requires:	libjpeg
Requires:	lirc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		addir	/usr/X11R6/lib/X11/app-defaults

%description
X11 TV application based on xawtv 2.x series with plugin capabilities.

%description -l pl
Aplikacja TV dla X11 oparta na xawtv 2.x z mo¿liwo¶ci± u¿ywania
wtyczek.

%package devel
Summary:	Development files for xawdecode
Summary(pl):	Pliki do programowania z u¿yciem xawdecode
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
Development files for xawdecode.

%description devel -l pl
Pliki do programowania z u¿yciem xawdecode.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{?_without_lirc:--disable-lirc} \
	%{!?_without_lirc:--enable-lirc} \
	--disable-divx4linux \
	--disable-alsa
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
/usr/X11R6/bin/mkfontdir                                                            

%postun
cd %{_fontsdir}/misc                                                            
umask 022                                                                       
/usr/X11R6/bin/mkfontdir                                                            

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQfr-xawdecode libavc-rate-control.txt
%doc lircrc.hauppauge.sample lircrc.miro.sample lisez-moi README*
%doc xawdecoderc.sample
%attr(755,root,root) %{_bindir}/xawdecode
%attr(4755,root,root) %{_bindir}/v4l-conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{addir}/*
%{_mandir}/man1/*
%{_fontsdir}/misc/*.pcf

%files devel
%defattr(644,root,root,755)
%{_includedir}/*

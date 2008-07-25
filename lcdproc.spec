# TODO:
# glcdproclib/glcdprocdriver.h
# widgets.h, usblcd.h and usblcd_util.h from the usblcd package
# ftdi library in version 0.7

Name:		lcdproc	
Version:	0.5.2
Release:	%mkrel 3
Summary: 	Displays real-time system information on a 20x4 backlit LCD
License:	GPL
URL:            http://lcdproc.omnipotent.net/
Group:     	Monitoring	
Source0:    	http://downloads.sourceforge.net/lcdproc/lcdproc-0.5.2.tar.gz
Source1:	LCDd.init
Requires(pre):	rpm-helper
Requires(preun): rpm-helper
BuildRequires:	docbook-utils-pdf
BuildRequires:  doxygen
BuildRequires:  g15-devel
BuildRequires:  g15daemon_client-devel
BuildRequires:  g15render-devel
BuildRequires:  graphviz
BuildRequires:  lirc-devel
BuildRequires:	ncurses-devel
BuildRequires:  svgalib-devel
BuildRequires:  tetex-latex
BuildRequires:	libusb-devel
BuildRequires:  xosd-devel
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
LCDproc is a client/server suite inclduding drivers for all
kinds of nifty LCD displays. The server supports several
serial devices: Matrix Orbital, Crystal Fontz, Bayrad, LB216, 
LCDM001 (kernelconcepts.de), Wirz-SLI and PIC-an-LCD; and some 
devices connected to the LPT port: HD44780, STV5730, T6963, 
SED1520 and SED1330. Various clients are available that display 
things like CPU load, system load, memory usage, uptime, and a lot more. 
See also http://lcdproc.omnipotent.net. 

%prep
%setup -q
%{__perl} -pi -e 's:../../../libirman-0.4.1b/irman.h:%{_includedir}/irman.h:g' server/drivers/irmanin.c

%build
%{configure2_5x} --disable-dependency-tracking \
                 --enable-libusb \
                 --enable-drivers=all \
                 --enable-seamless-hbars \
                 --enable-testmenus \
                 --enable-permissive-menu-goto \
                 --enable-lcdproc-menus \
                 --enable-stat-nfs \
                 --enable-stat-smbfs \
                 --enable-doxygen \
                 --enable-dot \
                 --enable-html-dox \
                 --enable-latex-dox
%{make}
%{make} dox

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

# init
install -d 		$RPM_BUILD_ROOT%{_initrddir}
install %{SOURCE1}	$RPM_BUILD_ROOT%{_initrddir}/LCDd

# Move examples in %_bindir like previous release
install clients/examples/*.pl $RPM_BUILD_ROOT%{_bindir}

# conf files
install -d		$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc
install LCDd.conf 	$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/LCDd.conf
touch scripts/lcdproc.conf  	$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/lcdproc.conf
echo "-s localhost -p 13666 C M X U P S" > \
			$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/lcdproc.conf

# doc files
cd docs/lcdproc-user
mkdir html txt pdf
#docbook2html -c %{_sysconfdir}/sgml/catalog -o html lcdproc-user.docbook
#docbook2pdf -c %{_sysconfdir}/sgml/catalog -o pdf lcdproc-user.docbook

%post
%_post_service LCDd

%preun
%_preun_service LCDd


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc README* INSTALL COPYING TODO ChangeLog
#%doc docs/lcdproc-user/html docs/lcdproc-user/pdf/*.pdf
#%doc docs/html/* docs/latex/
%defattr(-,root,root,0755)
%{_bindir}/*
%attr(0755,root,root) %{_initrddir}/LCDd
%{_libdir}/%{name}
%{_mandir}/man*/*
%{_sbindir}/*
%dir %{_sysconfdir}/lcdproc
%config(noreplace) %{_sysconfdir}/lcdproc/*
%config(noreplace) %{_sysconfdir}/LCDd.conf
%config(noreplace) %{_sysconfdir}/lcdexec.conf
%config(noreplace) %{_sysconfdir}/lcdproc.conf
%config(noreplace) %{_sysconfdir}/lcdvc.conf

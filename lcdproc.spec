# TODO:
# glcdproclib/glcdprocdriver.h
# widgets.h, usblcd.h and usblcd_util.h from the usblcd package
# ftdi library in version 0.7

Name:		lcdproc	
Version:	0.5.3
Release:	2
Summary: 	Displays real-time system information on a 20x4 backlit LCD
License:	GPLv2+
URL:    	http://lcdproc.omnipotent.net/
Group:     	Monitoring	
Source0:    	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	LCDd.init
Patch0: 	slow-down-imonlcd-0038.patch
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
%autopatch -p1

%build
unset LDFLAGS
./configure --disable-dependency-tracking \
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
%{makeinstall}

# init
install -d 		$RPM_BUILD_ROOT%{_initrddir}
install %{SOURCE1}	$RPM_BUILD_ROOT%{_initrddir}/LCDd

# Move examples in %_bindir like previous release
install -d              $RPM_BUILD_ROOT%{_bindir}
install clients/examples/*.pl $RPM_BUILD_ROOT%{_bindir}

# conf files
install -d		$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc
install LCDd.conf 	$RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/LCDd.conf
# fix path to drivers
perl -pi -e 's|DriverPath=.*/|DriverPath=/usr/lib/lcdproc/|' $RPM_BUILD_ROOT%{_sysconfdir}/lcdproc/LCDd.conf
# remove unwanted conf file (not used in initscript)
rm -vf $RPM_BUILD_ROOT%{_sysconfdir}/LCDd.conf
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
%config(noreplace) %{_sysconfdir}/lcdexec.conf
%config(noreplace) %{_sysconfdir}/lcdproc.conf
%config(noreplace) %{_sysconfdir}/lcdvc.conf


%changelog
* Sun Jan 02 2011 Maarten Vanraes <alien@mandriva.org> 0.5.3-1mdv2011.0
+ Revision: 627542
- update to newer 0.5.3
- patch imonlcd to slow down commands for device 0038

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.2-6mdv2011.0
+ Revision: 612709
- the mass rebuild of 2010.1 packages

* Mon Jan 25 2010 Antoine Ginies <aginies@mandriva.com> 0.5.2-5mdv2010.1
+ Revision: 496288
- use %%makeinstall macro
- fix path to drivers
- create missing %%_bindir
- fix BUILD process
- fix DriverPath in LCDd.conf file
- remove un-used configration file (we use the one in /etc/lcdproc)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

* Fri Feb 08 2008 David Walluck <walluck@mandriva.org> 0.5.2-1mdv2008.1
+ Revision: 163964
- 0.5.2
- enable as many drivers/features as possible

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.5.0-1mdv2008.1
+ Revision: 136535
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot


* Mon Aug 14 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/14/06 14:30:16 (56023)
- 0.5.0
- fix prereq

* Mon Aug 14 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 08/14/06 14:04:29 (56013)
Import lcdproc

* Mon Dec 15 2003 Arnaud de Lorbeau <devel@mandriva.com> 0.4.5-1mdk
- v0.4.5

* Fri Nov 21 2003 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 0.4.3-3mdk
- Rebuild


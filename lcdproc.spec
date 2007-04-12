Summary: 	LCDproc displays real-time system information on a 20x4 backlit LCD.
Name:   	lcdproc	
Version:	0.5.0
Release:	%mkrel 1
License:	GPL
Url:       	http://lcdproc.omnipotent.net
Group:     	Monitoring	
Source:    	%{name}-%{version}.tar.bz2
Source1:	LCDd.init
BuildRoot: 	%{_tmppath}/%{name}-buildroot
Requires(pre):		rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	libncurses-devel docbook-utils-pdf

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
rm -rf $RPM_BUILD_ROOT
%setup -q
perl -pi -e 's:../../../libirman-0.4.1b/irman.h:/usr/include/irman.h:g' server/drivers/irmanin.c

%build
%configure \
	--enable-stat-nfs \
	--enable-stat-smbfs \
	--enable-drivers='hd44780,lcdm001,curses,irman,text,lb216,bayrad,glk,joy,t6963,stv5730,sed1330,sed1520'

%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install

#%makeinstall
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# init
install -d 		$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install %SOURCE1	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/LCDd

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
#docbook2html -c /etc/sgml/catalog -o html lcdproc-user.docbook
#docbook2pdf -c /etc/sgml/catalog -o pdf lcdproc-user.docbook


%post
%_post_service LCDd

%preun
%_preun_service LCDd


%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man?/*
%dir 	%{_sysconfdir}/lcdproc
%_libdir/%name
%config(noreplace)	%{_sysconfdir}/lcdproc/*
%doc README* INSTALL COPYING TODO ChangeLog
#%doc docs/lcdproc-user/html docs/lcdproc-user/pdf/*.pdf
%defattr(-, root, root, 0700)
%config(noreplace)	%{_sysconfdir}/rc.d/init.d/LCDd


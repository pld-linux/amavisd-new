%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner with SpamAssasin support - Daemon.
Summary(pl):	Antywirusowy skaner poczty elektronicznej z obs³ug± SpamAssasina - Demon
Name:		amavisd-new
Version:	20020630
Release:	3
License:	GPL
Group:		Applications/Mail
Source0:	http://www.ijs.si/software/amavisd/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-notest-mta.patch
Patch1:		%{name}-nomilter.patch
Patch2:		%{name}-qmail.patch
Patch3:		%{name}-clamav.patch
Patch4:		%{name}-paths.patch
Patch5:		%{name}-avp.patch
URL:		http://www.ijs.si/software/amavisd/
BuildRequires:	arc
BuildRequires:	autoconf
BuildRequires:  automake
BuildRequires:	bzip2
BuildRequires:	file
BuildRequires:	lha
BuildRequires:	ncompress
BuildRequires:	perl-Archive-Tar
BuildRequires:	perl-Archive-Zip
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-MIME-tools
BuildRequires:	perl-Unix-Syslog
BuildRequires:	perl-Convert-UUlib
BuildRequires:	perl-Convert-TNEF
BuildRequires:	perl-libnet >= 1:1.12
BuildRequires:	perl-Mail-SpamAssassin
BuildRequires:	perl-Vipuls-Razor-V1
BuildRequires:	perl-Net-Server
BuildRequires:	sh-utils
BuildRequires:	unarj
BuildRequires:	unrar
BuildRequires:	zoo
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires:	/usr/lib/sendmail
Requires:	arc
Requires:	bzip2
Requires:	file
Requires:	lha
Requires:	ncompress
Requires:	sh-utils
Requires:	unarj
Requires:	unrar
Requires:	zoo
Requires:	perl-Mail-SpamAssassin
Requires:	perl-Vipuls-Razor-V1
Requires:	amavisd-new-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	AMaViS
Obsoletes:	amavis

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners and SpamAssasin.
This is daemonized version of amavis.

%description -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych i SpamAssasinem.
Wersja zdemonizowana.

%package postfix
Summary:	A Mail Virus Scanner with SpamAssasin support - postfix back-end.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - back-end dla postfiksa
Group:		Applications/Mail
Provides:	amavisd-new-daemon
Obsoletes:	amavisd-daemon
Obsoletes:	amavisd-new-daemon
Obsoletes:	amavisd-exim
Obsoletes:	amavisd-qmail
Obsoletes:	amavisd-sendmail
Requires:	postfix

%description postfix
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for postfix.

%description postfix -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla postfiks.

%package exim
Summary:	A Mail Virus Scanner with SpamAssasin support - exim backend.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla exima
Group:		Applications/Mail
Provides:	amavisd-new-daemon
Obsoletes:	amavisd-daemon
Obsoletes:	amavisd-new-daemon
Obsoletes:	amavisd-postfix
Obsoletes:	amavisd-qmail
Obsoletes:	amavisd-sendmail
Requires:	exim

%description exim
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for exim.

%description exim -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla exima.

# NFY
#%package qmail
#Summary:	A Mail Virus Scanner - qmail backend.
#Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla qmaila
#Group:		Applications/Mail
#Provides:	amavisd-new-daemon
#Obsoletes:	amavisd-daemon
#Obsoletes:	amavisd-new-daemon
#Obsoletes:	amavisd-postfix
#Obsoletes:	amavisd-exim
#Obsoletes:	amavisd-sendmail
#Requires:	qmailmta
#
#%description qmail
#AMaViS is a script that interfaces a mail transport agent (MTA) with
#one or more virus scanners. This is daemonized version of amavis.
#
#This package contains backend for qmail.
#
#%description qmail -l pl
#AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
#a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.
#
#Pakiet ten zawiera back-end dla qmaila.

%package sendmail
Summary:	A Mail Virus Scanner with SpamAssasin support - sendmail backend.
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla sendmaila
Group:		Applications/Mail
Provides:	amavisd-new-daemon
Obsoletes:	amavisd-daemon
Obsoletes:	amavisd-new-daemon
Obsoletes:	amavisd-postfix
Obsoletes:	amavisd-exim
Obsoletes:	amavisd-qmail
Requires:	sendmail

%description sendmail
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for sendmail.

%description sendmail -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla sendmaila.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
aclocal
%{__autoconf}
%{__automake}
%configure \
	--disable-smtp \
	--enable-exim \
	--enable-all \
	--enable-syslog \
	--with-smtp-port=10025 \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.exim

# NFY
#%%configure \
#	--disable-smtp \
#	--enable-qmail \
#	--enable-all \
#	--enable-syslog \
#	--with-smtp-port=10025 \
#	--with-runtime-dir=%{_var}/spool/amavis/runtime \
#	--with-virusdir=%{_var}/spool/amavis/virusmails \
#	--with-logdir=%{_var}/log \
#	--with-amavisuser=amavis \
#	--with-sockname=%{_var}/run/amavisd/amavisd.sock
#
#%{__make}
#mv amavis/amavisd amavis/amavisd.qmail

%configure \
	--disable-smtp \
	--enable-sendmail \
	--enable-all \
	--enable-syslog \
	--with-smtp-port=10025 \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.sendmail

%configure \
	--enable-smtp \
	--enable-postfix \
	--enable-all \
	--enable-syslog \
	--with-smtp-port=10025 \
	--with-runtime-dir=%{_var}/spool/amavis/runtime \
	--with-virusdir=%{_var}/spool/amavis/virusmails \
	--with-logdir=%{_var}/log \
	--with-amavisuser=amavis \
	--with-sockname=%{_var}/run/amavisd/amavisd.sock

%{__make}
mv amavis/amavisd amavis/amavisd.postfix

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis/{runtime,virusmails},%{_var}/run/amavisd}

%{__make} install \
	amavisuser=$(id -u) \
	DESTDIR=$RPM_BUILD_ROOT
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/amavisd

install amavis/amavisd.{exim,postfix,sendmail} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`id -u amavis 2>/dev/null`" ]; then
	if [ "`id -u amavis`" != "97" ]; then
		echo "Error: user amavis doesn't have uid=97. Correct this before installing amavis." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 97 -r -d %{_var}/spool/amavis -s /bin/false -c "Anti Virus Checker" -g nobody  amavis 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel amavis
fi

%post
/sbin/chkconfig --add amavisd
if [ -f /var/lock/subsys/amavisd ]; then
	/etc/rc.d/init.d/amavisd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/amavisd start\" to start Amavisd daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/amavisd ]; then
		/etc/rc.d/init.d/amavisd stop >&2
	fi
	/sbin/chkconfig --del amavisd
fi

%post exim
ln -sf amavisd.exim %{_sbindir}/amavisd

%post postfix
ln -sf amavisd.postfix %{_sbindir}/amavisd

#%post qmail
#ln -sf amavisd.qmail %{_sbindir}/amavisd

%post sendmail
ln -sf amavisd.sendmail %{_sbindir}/amavisd

%files
%defattr(644,root,root,755)
%doc README* NEWS AUTHORS BUGS ChangeLog FAQ HINTS TODO doc/amavis.html doc/amavis.png
%attr(755,root,root) %{_sbindir}/amavis
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/amavisd.conf
%attr(750,amavis,root) %{_var}/spool/amavis
%attr(755,amavis,root) %{_var}/run/amavisd

%files exim
%attr(755,root,root) %{_sbindir}/amavisd.exim
%ghost %attr(777,root,root) %{_sbindir}/amavisd

%files postfix
%attr(755,root,root) %{_sbindir}/amavisd.postfix
%ghost %attr(777,root,root) %{_sbindir}/amavisd

#%files qmail
#%attr(755,root,root) %{_sbindir}/amavisd.qmail
#%ghost %attr(777,root,root) %{_sbindir}/amavisd

%files sendmail
%attr(755,root,root) %{_sbindir}/amavisd.sendmail
%ghost %attr(777,root,root) %{_sbindir}/amavisd

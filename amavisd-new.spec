# TODO:
# - Add polish info mail templates
# - Some perl master check what Patch1 did 

%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner with SpamAssassin support - daemon
Summary(pl):	Antywirusowy skaner poczty elektronicznej z obs³ug± SpamAssasina - demon
Name:		amavisd-new
Version:	20030616
Release:	7
License:	GPL
Group:		Applications/Mail
Source0:	http://www.ijs.si/software/amavisd/%{name}-%{version}-p7.tar.gz
# Source0-md5:	e6f35be1e14861e3869debdd9bdfbfba
Source1:	%{name}.init
Patch0:		%{name}-config.patch
# Patch1:	%{name}-bin.patch # I don't get perl and it has rejects
Patch3:		%{name}-cpio-reads-tar.patch
URL:		http://www.ijs.si/software/amavisd/
BuildRequires:	arc
BuildRequires:	autoconf
BuildRequires:	automake
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
BuildRequires:	perl-libnet
BuildRequires:	perl-Mail-SpamAssassin
BuildRequires:	perl-Net-Server
BuildRequires:	sh-utils
BuildRequires:	unarj
BuildRequires:	unrar
BuildRequires:	zoo
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
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
#Requires:	perl-SAVI
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	AMaViS
Obsoletes:	amavis
Obsoletes:	amavisd
Obsoletes:	amavisd-daemon
Obsoletes:	amavisd-postfix
Obsoletes:	amavisd-exim
Obsoletes:	amavisd-qmail
Obsoletes:	amavisd-new-postfix
Obsoletes:	amavisd-new-exim
Obsoletes:	amavisd-new-qmail

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners and SpamAssasin. This is daemonized version
of amavis.

%description -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych i SpamAssasinem. Wersja
zdemonizowana.

%package sendmail
Summary:	A Mail Virus Scanner with SpamAssasin support - sendmail backend
Summary(pl):	Antywirusowy skaner poczty elektronicznej - backend dla sendmaila
Group:		Applications/Mail
Requires:	sendmail
Requires:	%{name}

%description sendmail
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for sendmail.

%description sendmail -l pl
AMaViS to skrypt po¶rednicz±cy pomiêdzy agentem transferu poczty (MTA)
a jednym lub wiêcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla sendmaila.

%prep
%setup -q
%patch0 -p1
#%%patch1 -p1
%patch3 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis/{runtime,virusmails},%{_var}/run/amavisd,%{_sysconfdir}/rc.d/init.d,%{_sbindir}}

install amavisd $RPM_BUILD_ROOT%{_sbindir}
install amavisd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/amavisd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid amavis`" ]; then
	if [ "`getgid amavis`" != "116" ]; then
		echo "Error: group amavis doesn't have gid=116. Correct this before installing amavisd-new." 1>&2
		exit 1
	fi
else
	echo "adding group amavis GID=116."
	/usr/sbin/groupadd -g 116 -r -f amavis
fi

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
	echo "Removing group amavis."
	/usr/sbin/groupdel amavis
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

%files
%defattr(644,root,root,755)
%doc AAAREADME.first INSTALL RELEASE_NOTES README_FILES/* test-messages
%attr(755,root,root) %{_sbindir}/amavisd*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/amavisd.conf
%attr(750,amavis,amavis) %{_var}/spool/amavis
%attr(755,amavis,root) %{_var}/run/amavisd

#%files sendmail
#%attr(755,root,root) %{_sbindir}/amavis
#%attr(755,root,root) %{_sbindir}/amavis-milter

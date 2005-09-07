# TODO:
# - Add polish info mail templates
%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner with SpamAssassin support - daemon
Summary(pl):	Antywirusowy skaner poczty elektronicznej z obs³ug± SpamAssasina - demon
Name:		amavisd-new
Version:	2.3.3
Release:	3
Epoch:		1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.ijs.si/software/amavisd/%{name}-%{version}.tar.gz
# Source0-md5:	0b02df514c1a2bf8af346bc9c7e97111
Source1:	%{name}.init
Source2:	%{name}-milter.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-dirperms.patch
Patch2:		%{name}-lib64.patch
Patch3:		%{name}-tools-dbdir.patch
URL:		http://www.ijs.si/software/amavisd/
BuildRequires:	autoconf
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sendmail-devel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires:	perl-Archive-Tar
Requires:	perl-Archive-Zip
Requires:	perl-Compress-Zlib >= 1.35
Requires:	perl-Convert-TNEF
Requires:	perl-Convert-UUlib
Requires:	perl-libnet
Requires:	perl-Mail-SpamAssassin
Requires:	perl-MIME-tools
Requires:	perl-Net-Server
Requires:	perl-Unix-Syslog
Requires:	sh-utils
Requires:	/usr/lib/sendmail
Provides:	group(amavis)
Provides:	user(amavis)
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
Conflicts:	amavis-stats <= 0.1.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	%{name} = %{epoch}:%{version}-%{release}
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
%setup -q
%patch0 -p1
# %patch1 -p1
%if "%{_lib}" == "lib64"
%patch2 -p1
%endif
%patch3 -p1

%build
cd helper-progs
%{__autoconf}
./configure \
	--with-sendmail=/usr/lib/sendmail \
	--with-runtime-dir=/var/spool/amavis/runtime \
	--with-sockname=/var/run/amavisd/amavisd.sock
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis/{runtime,virusmails,db},%{_var}/run/amavisd,/etc/rc.d/init.d,%{_sbindir}}

install amavisd $RPM_BUILD_ROOT%{_sbindir}
install amavisd-agent $RPM_BUILD_ROOT%{_sbindir}
install amavisd-nanny $RPM_BUILD_ROOT%{_sbindir}
install amavisd.conf-sample $RPM_BUILD_ROOT%{_sysconfdir}/amavisd.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/amavisd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/amavis-milter
install helper-progs/amavis $RPM_BUILD_ROOT%{_sbindir}
install helper-progs/amavis-milter $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 116 -r -f amavis
%useradd -u 97 -r -d %{_var}/spool/amavis -s /bin/false -c "Anti Virus Checker" -g amavis amavis

%postun
if [ "$1" = "0" ]; then
	%userremove amavis
	%groupremove amavis
fi

%post
/sbin/chkconfig --add amavisd
if [ -f /var/lock/subsys/amavisd ]; then
	/etc/rc.d/init.d/amavisd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/amavisd start\" to start Amavisd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/amavisd ]; then
		/etc/rc.d/init.d/amavisd stop >&2
	fi
	/sbin/chkconfig --del amavisd
fi

%post sendmail
/sbin/chkconfig --add amavis-milter
if [ -f /var/lock/subsys/amavis-milter ]; then
	/etc/rc.d/init.d/amavis-milter restart >&2
else
	echo "Run \"/etc/rc.d/init.d/amavis-milter start\" to start Amavis-milter daemon."
fi

%preun sendmail
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/amavis-milter ]; then
		/etc/rc.d/init.d/amavis-milter stop >&2
	fi
	/sbin/chkconfig --del amavis-milter
fi

%files
%defattr(644,root,root,755)
%doc AAAREADME.first INSTALL RELEASE_NOTES README_FILES/* test-messages
%attr(755,root,root) %{_sbindir}/amavisd*
%attr(754,root,root) /etc/rc.d/init.d/amavisd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavisd.conf
%attr(750,amavis,amavis) %{_var}/spool/amavis
%attr(750,amavis,amavis) %{_var}/run/amavisd

%files sendmail
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/amavis-milter
%attr(755,root,root) %{_sbindir}/amavis
%attr(755,root,root) %{_sbindir}/amavis-milter

# TODO:
# - Add polish info mail templates
# - move amavis part of tmpwatch configuration from tmpwatch.spec
#
%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner with SpamAssassin support - daemon
Summary(pl.UTF-8):	Antywirusowy skaner poczty elektronicznej z obsługą SpamAssasina - demon
Name:		amavisd-new
Version:	2.8.1
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.ijs.si/software/amavisd/%{name}-%{version}.tar.xz
# Source0-md5:	d6a9269438ef6ff43ca94ce9ace77afc
Source1:	%{name}.init
Source2:	%{name}.tmpfiles
Source3:	%{name}.tmpwatch
Source4:	%{name}.service
Patch0:		%{name}-config.patch
Patch1:		%{name}-tools-dbdir.patch
URL:		http://www.ijs.si/software/amavisd/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	tar >= 1:1.22
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	/usr/lib/sendmail
Requires:	perl-Archive-Tar
Requires:	perl-Archive-Zip >= 1.14
Requires:	perl-Convert-BinHex
Requires:	perl-Convert-TNEF
Requires:	perl-Convert-UUlib >= 1.05
Requires:	perl-IO-Compress
Requires:	perl-MIME-tools
Requires:	perl-Net-Server >= 0.93
Requires:	perl-Time-HiRes >= 1.49
Requires:	perl-Unix-Syslog
Requires:	perl-libnet
Requires:	rc-scripts >= 0.4.1.23
Requires:	sh-utils
Requires:	systemd-units >= 38
Suggests:	amavisd-milter >= 1.5.0
#Suggests:	arc
#Suggests:	arj
Suggests:	binutils
Suggests:	bzip2
Suggests:	cabextract
Suggests:	clamav
Suggests:	cpio
Suggests:	dspam
Suggests:	freeze
Suggests:	gzip
Suggests:	lha
Suggests:	lzop
#Suggests:	melt
Suggests:	ncompress
Suggests:	nomarch
Suggests:	pax
Suggests:	perl-Authen-SASL
Suggests:	unarj
#Suggests:	unfreeze
# required already by perl-Mail-SpamAssassin
#Suggests:	perl-DB_File
#Suggests:	perl-IO-Socket-INET6
# required when doing SQL lookups
Suggests:	p0f
#Suggests:	perl-DBD-mysql
Suggests:	perl-Digest-MD5
Suggests:	perl-Mail-DKIM >= 0.31
Suggests:	perl-Mail-SpamAssassin > 3.3.0
Suggests:	perl-Razor
Suggests:	perl-SAVI
Suggests:	perl-ldap
#Suggests:	rar
#Suggests:	ripole
Suggests:	rpm-utils
Suggests:	tnef
Suggests:	unrar
Suggests:	unzoo
#Suggests:	zoo
Provides:	group(amavis)
Provides:	user(amavis)
Obsoletes:	AMaViS
Obsoletes:	amavis
Obsoletes:	amavisd
Obsoletes:	amavisd-daemon
Obsoletes:	amavisd-exim
Obsoletes:	amavisd-new-exim
Obsoletes:	amavisd-new-postfix
Obsoletes:	amavisd-new-qmail
Obsoletes:	amavisd-postfix
Obsoletes:	amavisd-qmail
Conflicts:	amavis-stats <= 0.1.12
Conflicts:	postfix < 2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_tmpwatchdir	/etc/tmpwatch
%define		schemadir	/usr/share/openldap/schema

%description
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners and SpamAssasin. This is daemonized version
of amavis.

%description -l pl.UTF-8
AMaViS to skrypt pośredniczący pomiędzy agentem transferu poczty (MTA)
a jednym lub więcej programów antywirusowych i SpamAssasinem. Wersja
zdemonizowana.

%package -n openldap-schema-amavisd-new
Summary:	Amavisd-new LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla amavisd-new
Group:		Networking/Daemons
Requires:	openldap-servers
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n openldap-schema-amavisd-new
This package contains LDAP schema for use with amavisd-new.

%description -n openldap-schema-amavisd-new -l pl.UTF-8
Ten pakiet zawiera schemat LDAP do używania z amavisd-new.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_var}/spool/amavis/{runtime,virusmails,db} \
	$RPM_BUILD_ROOT{%{_var}/run/amavisd,/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT{/usr/lib/tmpfiles.d,%{_tmpwatchdir}} \
	$RPM_BUILD_ROOT%{systemdunitdir}

install -p amavisd $RPM_BUILD_ROOT%{_sbindir}
install -p amavisd-agent $RPM_BUILD_ROOT%{_sbindir}
install -p amavisd-nanny $RPM_BUILD_ROOT%{_sbindir}
install -p amavisd-release $RPM_BUILD_ROOT%{_sbindir}
install -p amavisd-submit $RPM_BUILD_ROOT%{_sbindir}
cp -p amavisd.conf $RPM_BUILD_ROOT%{_sysconfdir}/amavisd.conf

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/amavisd
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_tmpwatchdir}/%{name}.conf

install %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/amavisd.service

install -Dp LDAP.schema $RPM_BUILD_ROOT%{schemadir}/amavisd-new.schema

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
%systemd_reload

%post
/sbin/chkconfig --add amavisd
%service amavisd restart "Amavisd daemon"
%systemd_post amavisd.service

%preun
if [ "$1" = "0" ]; then
	%service amavisd stop
	/sbin/chkconfig --del amavisd
fi
%systemd_preun amavisd.service

%triggerpostun -- %{name} < 1:2.8.1-1
%systemd_trigger amavisd.service

%post -n openldap-schema-amavisd-new
%openldap_schema_register %{schemadir}/amavisd-new.schema
%service -q ldap restart

%postun -n openldap-schema-amavisd-new
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/amavisd-new.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%doc AAAREADME.first INSTALL RELEASE_NOTES README_FILES/* test-messages
%attr(755,root,root) %{_sbindir}/amavisd
%attr(755,root,root) %{_sbindir}/amavisd-agent
%attr(755,root,root) %{_sbindir}/amavisd-nanny
%attr(755,root,root) %{_sbindir}/amavisd-release
%attr(755,root,root) %{_sbindir}/amavisd-submit
%{systemdunitdir}/amavisd.service
%attr(754,root,root) /etc/rc.d/init.d/amavisd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavisd.conf
%config(noreplace) %verify(not md5 mtime size) %{_tmpwatchdir}/%{name}.conf
/usr/lib/tmpfiles.d/%{name}.conf
%attr(750,amavis,amavis) %{_var}/spool/amavis
%attr(750,amavis,amavis) %{_var}/run/amavisd

%files -n openldap-schema-amavisd-new
%defattr(644,root,root,755)
%{schemadir}/*.schema

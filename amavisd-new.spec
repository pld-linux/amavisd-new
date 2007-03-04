# TODO:
# - Add polish info mail templates
# - move amavis part of tmpwatch configuration from tmpwatch.spec
#
%include	/usr/lib/rpm/macros.perl
Summary:	A Mail Virus Scanner with SpamAssassin support - daemon
Summary(pl.UTF-8):	Antywirusowy skaner poczty elektronicznej z obsługą SpamAssasina - demon
Name:		amavisd-new
Version:	2.4.5
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.ijs.si/software/amavisd/%{name}-%{version}.tar.gz
# Source0-md5:	eef8c03855f9e3a4c6c53c06006d77ea
Source1:	%{name}.init
Source2:	%{name}-milter.init
Source3:	%{name}.tmpwatch
Patch0:		%{name}-config.patch
Patch1:		%{name}-tools-dbdir.patch
URL:		http://www.ijs.si/software/amavisd/
BuildRequires:	autoconf
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	libmilter-devel
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
Requires:	perl-Compress-Zlib >= 1.35
Requires:	perl-Convert-TNEF
Requires:	perl-Convert-UUlib >= 1.05
Requires:	perl-MIME-tools
Requires:	perl-Mail-SpamAssassin
Requires:	perl-Net-Server >= 0.93
Requires:	perl-Time-HiRes >= 1.49
Requires:	perl-Unix-Syslog
Requires:	perl-libnet
Requires:	sh-utils
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

%package sendmail
Summary:	A Mail Virus Scanner with SpamAssasin support - sendmail backend
Summary(pl.UTF-8):	Antywirusowy skaner poczty elektronicznej - backend dla sendmaila
Group:		Applications/Mail
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	sendmail

%description sendmail
AMaViS is a script that interfaces a mail transport agent (MTA) with
one or more virus scanners. This is daemonized version of amavis.

This package contains backend for sendmail.

%description sendmail -l pl.UTF-8
AMaViS to skrypt pośredniczący pomiędzy agentem transferu poczty (MTA)
a jednym lub więcej programów antywirusowych. Wersja zdemonizowana.

Pakiet ten zawiera back-end dla sendmaila.

%package -n openldap-schema-amavisd-new
Summary:	Amavisd-new LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla amavisd-new
Group:		Networking/Daemons
Requires:	openldap-servers

%description -n openldap-schema-amavisd-new
This package contains LDAP schema for use with amavisd-new.

%description -n openldap-schema-amavisd-new -l pl.UTF-8
Ten pakiet zawiera schemat LDAP do używania z amavisd-new.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd helper-progs
%configure \
	--with-sendmail=/usr/lib/sendmail \
	--with-runtime-dir=/var/spool/amavis/runtime \
	--with-sockname=/var/run/amavisd/amavisd.sock \
	--with-milterlib=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/spool/amavis/{runtime,virusmails,db},%{_var}/run/amavisd,/etc/rc.d/init.d,%{_sbindir},%{_tmpwatchdir}}

install amavisd $RPM_BUILD_ROOT%{_sbindir}
install amavisd-agent $RPM_BUILD_ROOT%{_sbindir}
install amavisd-nanny $RPM_BUILD_ROOT%{_sbindir}
install amavisd.conf-sample $RPM_BUILD_ROOT%{_sysconfdir}/amavisd.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/amavisd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/amavis-milter
install helper-progs/amavis $RPM_BUILD_ROOT%{_sbindir}
install helper-progs/amavis-milter $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_tmpwatchdir}/%{name}.conf
install -D LDAP.schema $RPM_BUILD_ROOT%{schemadir}/amavisd-new.schema

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
%service amavisd restart "Amavisd daemon"

%preun
if [ "$1" = "0" ]; then
	%service amavisd stop
	/sbin/chkconfig --del amavisd
fi

%post sendmail
/sbin/chkconfig --add amavis-milter
%service amavis-milter restart "Amavis-milter daemon"

%preun sendmail
if [ "$1" = "0" ];then
	%service amavis-milter stop
	/sbin/chkconfig --del amavis-milter
fi

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
%attr(755,root,root) %{_sbindir}/amavisd*
%attr(754,root,root) /etc/rc.d/init.d/amavisd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amavisd.conf
%config(noreplace) %verify(not md5 mtime size) %{_tmpwatchdir}/%{name}.conf
%attr(750,amavis,amavis) %{_var}/spool/amavis
%attr(750,amavis,amavis) %{_var}/run/amavisd

%files sendmail
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/amavis-milter
%attr(755,root,root) %{_sbindir}/amavis
%attr(755,root,root) %{_sbindir}/amavis-milter

%files -n openldap-schema-amavisd-new
%defattr(644,root,root,755)
%{schemadir}/*.schema

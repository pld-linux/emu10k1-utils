%define epache_version	0.1.4
Summary:	Utils controlling emu10k1 processor
Summary(pl):	Narzêdzia kontroluj±ce procesor emu10k1
Name:		emu10k1-utils
Version:	0.9.4
Release:	7
License:	GPL
Group:		Applications/Sound
Source0:	http://dl.sourceforge.net/emu10k1/emu-tools-%{version}.tar.gz
# Source0-md5:	906fc53ad142bb4d3531c941d7878264
Source1:	http://www.geocities.com/hsokolow2001/linux/epache-%{epache_version}.tgz
# Source1-md5:	f85a9f71485a4f8667084010e7c18e6f
Source2:	m2049.pdf
Source3:	hog63.ps
Patch0:		%{name}-path.patch
Patch1:		%{name}-aumix.patch
Patch2:		%{name}-fv10k1.patch
Patch3:		%{name}-gcc33.patch
Patch4:		%{name}-nokernel.patch
URL:		http://sourceforge.net/projects/emu10k1/
BuildRequires:	gtk+-devel
BuildRequires:	libstdc++-devel
BuildRequires:	m4
BuildRequires:	perl-base
Conflicts:	alsa-driver
Conflicts:	kernel < 2.4.11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The emu10k1 is really a dsp processor. It does not do any effects on
it's own, nor does it route sound from input to output. We had to
write dsp code to do that ourselves. emu10k1-utils allows us to set
routing, load/unload patches (aka effects), control GPRs, map mixer
elements.

This package contains emu-dspmgr, a tool for configuring the cards dsp
patch management system and emu-config, a configuration tool for
emu10k1 based sound cards. Also, several ".bin" dsp patches will be
installed. You can load these patches using emu-dspmgr.

%description -l pl
emu10k1 jest w rzeczywisto¶ci procesorem sygna³ów cyfrowych (dsp). Nie
robi ¿adnych efektów sam z siebie, ani nie kieruje d¼wiêku z wej¶cia
na wyj¶cie. Odpowiedzialny za to kod dsp musi byæ napisany i
za³adowany. emu10k1-utils pozwala ustawiæ routing, (za/wy)³adowaæ
³atki (efekty), kontrolowaæ ich parametry (np. przez odzwierciedlenie
w mikserze).

Ten pakiet zawiera emu-dspmgr, narzêdzie obs³uguj±ce system
zarz±dzania ³atkami dsp karty i emu-config, konfigurator kart
d¼wiêkowych opartych na emu10k1. Zainstalowane zostanie równie¿ kilka
gotowych, skompilowanych ³atek, które mo¿na za³adowaæ u¿ywaj±c
emu-dspmgr.

%package devel
Summary:	emu10k1 programming utils
Summary(pl):	Narzêdzia do programowania emu10k1
Group:		Applications/Sound

%description devel
Package contains:
- as10k1 - Assembler for the emu10k1 DSP Processor
- patches sources

%description devel -l pl
Pakiet zawiera:
- as10k1 - asembler dla procesora emu10k1
- ¼ród³a ³atek z g³ównego pakietu

%package autoconfig
Summary:	emu10k1 autoconfiguration on module load
Summary(pl):	Skrypt konfiguruj±cy emu10k1 przy ³adowaniu modu³u
Group:		Applications/Sound
Requires(triggerpostun):	sed >= 4.0
Requires:	%{name} = %{version}-%{release}
Requires:	aumix
Requires:	module-init-tools >= 3.2.2-2

%description autoconfig
Script loading patches. Currently it cannot do too much.

%description autoconfig -l pl
Skrypt ³aduj±cy ³atki. W chwili obecnej nie potrafi zbyt du¿o.

%package epache
Summary:	Program for configuring patches for emu10k1 based sound cards
Summary(pl):	Program konfiguruj±cy ³atki dla kart opartych na emu10k1
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description epache
- with the help of emu-dspmgr you can easily load a patch to the card
  on the specified line (the patch must be generated with the as10k1
  assembler) and clean the card from it.
- you can control 'CONTROL GPRS' of loaded patches (such as speed in
  flanger)
- you can save sessions and load them later, session is a list of
  patches currenlty loaded with values of controls.

%description epache -l pl
- z pomoc± emu-dspmgra mo¿esz ³atwo ³adowaæ ³aty do karty na dan±
  liniê (³ata musi byæ wygenerowana przez asembler as10k1) oraz
  wyczy¶ciæ z niej kartê,
- mo¿esz kontrolowaæ rejestry kontrolne za³adowanych ³at,
- mo¿esz zachowywaæ sesje i ³adowaæ je; sesja jest list± aktualnie
  za³adowanych ³at z warto¶ciami kontrolnymi.

%prep
%setup -n emu-tools-%{version} -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cp %{SOURCE2} %{SOURCE3} .

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -W -Wall"

cd dbgemu
%{__cc} %{rpmldflags} %{rpmcflags} -Wall -o dbgemu dbgemu.c

cd ../fv10k1
%{__cxx} %{rpmldflags} %{rpmcflags} -Wall -o calcroom calcroom.C
%{__make}
cd ..

%{__make} -C epache-%{epache_version} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall \$(GTK_CFLAGS)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install epache-%{epache_version}/epache $RPM_BUILD_ROOT%{_bindir}
install dbgemu/dbgemu $RPM_BUILD_ROOT%{_bindir}
mv dbgemu/README dbgemu/README.dbgemu
install as10k1/effects/*.asm $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm
install as10k1/effects/*.inc $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm

gzip -9nf $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/*
gzip -9nf $RPM_BUILD_ROOT%{_datadir}/emu10k1/README
install -d $RPM_BUILD_ROOT/etc/modprobe.d
cat <<'EOF' > $RPM_BUILD_ROOT/etc/modprobe.d/%{name}.conf
install emu10k1 /sbin/modprobe --ignore-install emu10k1 && { /usr/bin/emu-script; }
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun autoconfig -- emu10k1-utils-autoconfig < 0.9.4-6.1
%{__sed} -i -e '/install emu10k1 /d' /etc/modprobe.conf

%files
%defattr(644,root,root,755)
%doc docs/CHANGES docs/README docs/README.FAQ dbgemu/README.dbgemu
%attr(754,root,root) %{_bindir}/emu-config
%attr(754,root,root) %{_bindir}/emu-dspmgr
%attr(754,root,root) %{_bindir}/dbgemu
%dir %{_datadir}/emu10k1
%{_datadir}/emu10k1/*.bin
%{_datadir}/emu10k1/README.gz
%{_mandir}/man1/emu-*

%files devel
%defattr(644,root,root,755)
%doc docs/dsp.txt docs/manuals.txt docs/multichannel.txt docs/TODO hog63.ps m2049.pdf
%attr(755,root,root) %{_bindir}/as10k1
%{_datadir}/emu10k1/asm
%{_mandir}/man1/as10k1*

%files autoconfig
%defattr(644,root,root,755)
%attr(754,root,root) %{_bindir}/emu-script
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/emu10k1.conf

%files epache
%defattr(644,root,root,755)
%doc epache-%{epache_version}/README
%attr(755,root,root) %{_bindir}/epache

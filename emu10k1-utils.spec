%define snap	20020101
Summary:	Utils controlling emu10k1 processor
Summary(pl):	Narzêdzia kontroluj±ce procesor emu10k1
Name:		emu10k1-utils
Version:	0.9.3
Release:	0.%{snap}.1
License:	GPL
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(es):	Aplicaciones/Sonido
Group(pl):	Aplikacje/D¼wiêk
Group(pt_BR):	Aplicações/Som
Source0:	%{name}-%{snap}.tar.bz2
Patch0:		%{name}-path.patch
Patch1:		%{name}-aumix.patch
Patch2:		%{name}-fv10k1.patch
URL:		http://opensource.creative.com/
# czy w j±drach 2.2 jest obs³uga emu10k1? jak nie, to dodaæ requires: kernel >=2.4
BuildRequires:	m4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr

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
za³adowany. emu10k1-utils pozwala ustawiæ routing, (za/wy)³adowywaæ
³atki (efekty), kontrolowaæ ich parametry (np. przez odzwierciedlenie
w mikserze).

Ten pakiet zawiera emu-dspmgr, narzêdzie obs³uguj±ce system
zarz±dzania ³atkami dsp karty i emu-config, konfigurator kart
d¼wiêkowych opartych na emu10k1. Zainstalowane zostanie równie¿ kilka
gotowych, skompilowanych ³atek, które mo¿na za³adowaæ u¿ywaj±c
emu-dspmgr.

%package devel
Summary:	emu10k1 programming utils.
Summary(pl):	Narzêdzia do programowania emu10k1
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(es):	Aplicaciones/Sonido
Group(pl):	Aplikacje/D¼wiêk
Group(pt_BR):	Aplicações/Som

%description devel
Package contains:
- as10k1 - Assembler for the emu10k1 DSP Processor
- patches sources

%description -l pl devel
Pakiet zawiera:
- as10k1 - asembler dla procesora emu10k1
- ¼ród³a ³atek z g³ównego pakietu

%package autoconfig
Summary:	emu10k1 autoconfiguration on module load.
Summary(pl):	Skrypt konfiguruj±cy emu10k1 przy ³adowaniu modu³u.
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(es):	Aplicaciones/Sonido
Group(pl):	Aplikacje/D¼wiêk
Group(pt_BR):	Aplicações/Som
Requires:	%{name} = %{version}
Requires:	aumix

%description autoconfig
Script loading patches. Currently it cannot do too much.

%description -l pl autoconfig
Skrypt ³aduj±cy ³atki. W chwili obecnej nie potrafi zbyt du¿o.

%prep
%setup -n emu10k1-utils -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make}
#%{__make} -C compiler
#%{__make} -C dbgemu
%{__make} -C fv10k1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install
cp fv10k1/load.sh fv10k1/unload.sh fv10k1/fv10k1control.pl $RPM_BUILD_ROOT%{_bindir}
mv fv10k1/README docs/README.fv10k1
cp fv10k1/bin/* $RPM_BUILD_ROOT%{_datadir}/emu10k1/
mkdir $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/
cp fv10k1/*.asm $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/
cp fv10k1/*.inc $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/
cp as10k1/effects/*.asm $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/
cp -f as10k1/effects/*.inc $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/
gzip -9nf $RPM_BUILD_ROOT%{_datadir}/emu10k1/asm/*

gzip -9nf $RPM_BUILD_ROOT%{_datadir}/emu10k1/README
gzip -9nf docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	autoconfig
grep "post-install emu10k1 /usr/bin/emu-script" /etc/modules.conf > /dev/null
if [ "$?" -eq "1" ]
then
	echo "post-install emu10k1 /usr/bin/emu-script" >> /etc/modules.conf
fi

%postun	autoconfig
grep -v "post-install emu10k1 /usr/bin/emu-script" /etc/modules.conf > /etc/modules.conf.new
mv -f /etc/modules.conf /etc/modules.conf.old
mv /etc/modules.conf.new /etc/modules.conf

%files
%defattr(644,root,root,755)
%attr(750,root,root) %{_bindir}/emu-config
%attr(750,root,root) %{_bindir}/emu-dspmgr
%attr(750,root,root) %{_bindir}/fv10k1control.pl
%attr(750,root,root) %{_bindir}/load.sh
%attr(750,root,root) %{_bindir}/unload.sh
%doc docs/README-TOOLS.gz docs/README.fv10k1.gz
%{_mandir}/man1/emu-*
%dir %{_datadir}/emu10k1
%{_datadir}/emu10k1/*.bin
%{_datadir}/emu10k1/README.gz

%files devel
%defattr(644,root,root,755)
%attr(750,root,root) %{_bindir}/as10k1
%doc docs/dsp.txt.gz docs/manuals.txt.gz docs/registers.txt.gz docs/tram.txt.gz
%{_mandir}/man1/as10k1*
%dir %{_datadir}/emu10k1/asm
%{_datadir}/emu10k1/asm/*

%files autoconfig
%defattr(644,root,root,755)
%attr(750,root,root) %{_bindir}/emu-script
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/emu10k1.conf

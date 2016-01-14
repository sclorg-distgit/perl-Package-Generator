%{?scl:%scl_package perl-Package-Generator}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Package-Generator
Version:	1.105
Release:	7.sc1%{?dist}
Summary:	Generate new packages quickly and easily
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Package-Generator/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Package-Generator-%{version}.tar.gz
Patch1:		Package-Generator-1.105-old-Test::More.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Scalar::Util)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(File::Find)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(Params::Util) >= 0.11
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.47
# Extra Tests
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

# We need to patch the test suite if we have an old version of Test::More
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.88) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)}

%description
This module lets you quickly and easily construct new packages. It gives
them unused names and sets up their package data, if provided.

%prep
%setup -q -n Package-Generator-%{version}

# We need to patch the test suite if we have an old version of Test::More
%if 00%{old_test_more}
%patch1
%endif

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%{?scl:scl enable %{scl} - << \EOF}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%{?scl:EOF}

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Package/
%{_mandir}/man3/Package::Generator.3pm*
%{_mandir}/man3/Package::Reaper.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.105-7
- Fixed getting of %%old_test_more
- Resolves: rhbz#1063206

* Mon Feb 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.105-6
- Update command for getting value of old_test_more
- Resolves: rhbz#1063206

* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.105-5
- Update command for getting value of old_test_more

* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.105-4
- Rebuilt for SCL

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.105-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.105-2
- Perl 5.18 rebuild

* Mon Jul  8 2013 Paul Howarth <paul@city-fan.org> - 1.105-1
- Update to 1.105
  - Repackage, update bug tracker
  - Drop pod tests
- Add patch to support building with Test::More < 0.88
- Classify buildreqs by usage
- Explicitly run the extra tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 24 2012 Paul Howarth <paul@city-fan.org> - 0.103-14
- Drop EPEL-4 support
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- BR: perl(File::Spec)

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 0.103-13
- Specify all dependencies
- Package LICENSE

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.103-11
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.103-10
- Perl 5.16 rebuild

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.103-9
- Don't BR: perl(Test::Perl::Critic) if we're bootstrapping

* Wed Feb  1 2012 Paul Howarth <paul@city-fan.org> - 0.103-8
- Run Perl::Critic test in %%check too
- BR: perl(Test::Perl::Critic)
- BR: perl(Carp) and perl(Symbol), which might be dual-lived
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop version requirement for perl(ExtUtils::MakeMaker); older versions work
  without problems, e.g. version 6.17 on EL-4
- Make %%files list more explicit
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.103-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.103-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.103-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.103-2
- Rebuild against perl 5.10.1

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.103-1
- Auto-update to 0.103 (by cpan-spec-update 0.01)
- Added a new br on perl(ExtUtils::MakeMaker) (version 6.42)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.102-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.102-1
- Rebuild for new perl
- Update to 0.102
- Fix license tag

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.100-2
- Bump

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.100-1
- Specfile autogenerated by cpanspec 1.69.1

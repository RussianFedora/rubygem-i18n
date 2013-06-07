%global gem_name i18n

%if 0%{?rhel} == 6 || 0%{?fedora} < 17
%define rubyabi 1.8
%else
%define rubyabi 1.9.1
%endif

%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir%{gem_instdir}/lib
%endif

%if 0%{?fedora}
BuildRequires: rubygems-devel
%endif

Summary: New wave Internationalization support for Ruby
Name: rubygem-%{gem_name}
Version: 0.6.1
Release: 3%{?dist}
Group: Development/Languages
License: MIT and (GPLv2 or Ruby)
URL: http://github.com/svenfuchs/i18n
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(rubygems)
Requires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(test_declarative)
# TODO: Circular dependency with active support.
#BuildRequires: rubygem(activesupport)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Ruby Internationalization and localization solution.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gem_dir}
# Avoid some encoding complaints.
# https://github.com/svenfuchs/i18n/issues/176
LANG=en_US.utf8 gem install --local --install-dir .%{gem_dir} \
            --force --rdoc %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
chmod -x %{buildroot}%{gem_instdir}/MIT-LICENSE
chmod -x %{buildroot}%{gem_libdir}/i18n.rb

%check
pushd .%{gem_instdir}

# Bundler just complicates everything in our case, remove it.
sed -i -e "s|require 'bundler/setup'||" test/test_helper.rb
# Tests are failing without LANG environment is set.
# https://github.com/svenfuchs/i18n/issues/115
LANG=en_US.utf8 testrb -Ilib test/all.rb
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/README.textile
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/CHANGELOG.textile
%{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/ci
%{gem_instdir}/test
%doc %{gem_docdir}


%changelog
* Mon Jan 14 2013 Eric D Helms <ehelms@redhat.com> 0.6.1-3
- Rubygem-i18n - Adding gem_libdir declaration. (ehelms@redhat.com)

* Mon Jan 14 2013 Eric D Helms <ehelms@redhat.com> 0.6.1-2
- Rubygem-i18n - Adding initial 0.6 version for Rails 3.2 support
  (ehelms@redhat.com)
- adding first bunch of rails deps (lzap+git@redhat.com)

* Fri Oct 26 2012 Vít Ondruch <vondruch@redhat.com> - 0.6.1-1
- Update to I18n 0.6.1.

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-1
- Update to I18n 0.6.0.
- Removed unneeded %%defattr usage.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.5.0-3
- Rebuilt for Ruby 1.9.3.
- Enabled test suite.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 Vít Ondruch <vondruch@redhat.com> - 0.5.0-1
- Update to i18n 0.5.0.
- Documentation moved into subpackage.
- Removed unnecessary cleanup.
- Preparetion for test suite execution during build.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-2
- Add GPLv2 or Ruby License
- Files MIT-LICENSE, geminstdir/lib/i18n.rb are non executable now

* Thu Nov 11 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.4.2-1
- Initial package

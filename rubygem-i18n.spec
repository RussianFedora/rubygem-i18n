%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname i18n
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

%global enable_check 0

Summary: New wave Internationalization support for Ruby
Name: rubygem-%{gemname}
Version: 0.6.1
Release: 1%{?dist}
Group: Development/Languages
License: MIT and (GPLv2 or Ruby)
URL: http://github.com/svenfuchs/i18n
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: rubygems
Requires: ruby(abi) = 1.8
BuildRequires: ruby(abi) = 1.8
BuildRequires: rubygems
%if %{enable_check} > 0
BuildRequires: rubygem(mocha)
# test_declarative is not available in Fedora yet.
BuildRequires: rubygem(test_declarative)
%endif
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

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
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --force --rdoc %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/
chmod -x %{buildroot}%{geminstdir}/MIT-LICENSE
chmod -x %{buildroot}%{geminstdir}/lib/i18n.rb

%if %{enable_check} > 0
%check
pushd .%{geminstdir}

# Bundler just complicates everything in our case, remove it.
sed -i -e "s|require 'bundler/setup'||" test/test_helper.rb

RUBYOPT="rubygems I%{buildroot}%{geminstdir}/lib" testrb test/all.rb

popd
%endif

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%{geminstdir}/lib
%doc %{geminstdir}/README.textile
%doc %{geminstdir}/MIT-LICENSE
%doc %{geminstdir}/CHANGELOG.textile
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{geminstdir}/ci
%{geminstdir}/test
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Mon Jun 10 2013 Sergey Mihailov <sergey.mihailov@gmail.com> - 0.6.1-1
- Update to version 0.6.1

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

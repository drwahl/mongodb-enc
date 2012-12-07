Name:           mongodb-enc
Version:        0.1
Release:        1%{dist}
Summary:        MongoDB driven External Node Classifier (ENC)
License:        GPLv3
URL:            https://github.com/bcarpio/mongodb-enc
Group:          System Environment/Base
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python
Requires:       pymongo
Requires:       PyYAML
Requires:       python-argparse

%description
A set of scripts which can be used to leverage mongodb as an external node
classifier for puppet.

%prep
%setup -q -n %{name}

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}/mongodb-enc
%{__mkdir_p} %{buildroot}%{_sysconfdir}/mongodb-enc
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/mongodb-enc
cp -r ./scripts/* %{buildroot}%{_bindir}/mongodb-enc/
cp -r ./conf/* %{buildroot}%{_sysconfidir}/mongodb-enc/

%files
%{_bindir}/mongodb-enc/*
%{_sysconfdir}/mongodb-enc/*

%pre

%post

%clean
rm -rf %{buildroot}

%changelog
* Thu Dec 6 2012 David Wahlstrom <dwahlstrom@classmates.com> - 0.1-1
- initial packaging of mongodb-enc

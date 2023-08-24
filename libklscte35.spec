Name:       libklscte35
Version:    1.0.0rc1
Release:    1%{dist}
Summary:    Kernel Labs SCTE 35 library.
License:    LGPLv2.1
Source0:    https://github.com/stoth68000/libklscte35/archive/refs/heads/master.zip

BuildRequires: make gcc autoconf automake libtool libklvanc-devel

%description
Kernel Labs SCTE 35 library.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. 

%package utils
Summary: Commandline tools for %{name}
Group: Video/Utilties
Requires: %{name} = %{version}-%{release}

%description utils
This package contains command-line utilities for %{name}. 

%prep

#%setup -q -n %{name}-%{version}
%setup -q -n %{name}-master

%build

./autogen.sh --build
%configure \
	--enable-shared \
	--enable-static

make %{?_smp_mflags}

# check
# 
# make test

%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -delete

%clean

rm -rf $RPM_BUILD_ROOT

%files
/usr/lib64/libklscte35.so.0
/usr/lib64/libklscte35.so.0.0.0

%files utils
/usr/bin/klscte35_parse
/usr/bin/klscte35_scte104
/usr/bin/klscte35_scte104to35
/usr/bin/klscte35_util

%files devel
/usr/include/libklscte35/scte35.h
/usr/lib64/libklscte35.a
/usr/lib64/libklscte35.so

%changelog


%define vendor_name Intel
%define vendor_label intel
%define driver_name ice

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 1.6.4
Release: 1%{?dist}
License: GPLv2

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-ice/archive?at=1.6.4&format=tgz&prefix=driver-intel-ice-1.6.4#/intel-ice-1.6.4.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-intel-ice/archive?at=1.6.4&format=tgz&prefix=driver-intel-ice-1.6.4#/intel-ice-1.6.4.tar.gz) = f3b92b1169dafaea470f29442e1d17f593b6ecc0


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

DDP_PKG_DEST_PATH=%{buildroot}/lib/firmware/updates/%{vendor_label}/%{driver_name}/ddp
mkdir -p ${DDP_PKG_DEST_PATH}
install -m 644 $(pwd)/ddp/%{driver_name}-*.pkg ${DDP_PKG_DEST_PATH}
(cd ${DDP_PKG_DEST_PATH} && ln -sf %{driver_name}-*.pkg %{driver_name}.pkg)

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko
/lib/firmware/updates/*

%changelog
* Wed Jul 14 2021 Chuntian Xu <chuntian.xu@citrix.com> - 1.6.4-1
- CP-37345: Update ice driver to 1.6.4
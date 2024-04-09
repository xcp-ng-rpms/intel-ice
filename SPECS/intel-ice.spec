%global package_speccommit 023d3f40d725acb42cf9fc18674a78388145364d
%global usver 1.11.17.1
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 1.11.17.1
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
Version: 1.11.17.1
Release: %{?xsrel}%{?dist}
License: GPLv2
Source0: intel-ice-1.11.17.1.tar.gz
Patch0: fix-enabling-sr-iov-with-xen.patch

BuildRequires: gcc
BuildRequires: kernel-devel >= 4.19.19-8.0.29
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires: kernel >= 4.19.19-8.0.29
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

DDP_PKG_DEST_PATH=%{buildroot}/lib/firmware/updates/%{vendor_label}/%{driver_name}/ddp
mkdir -p ${DDP_PKG_DEST_PATH}
install -m 644 $(pwd)/ddp/%{driver_name}-*.pkg ${DDP_PKG_DEST_PATH}
(cd ${DDP_PKG_DEST_PATH} && ln -sf %{driver_name}-*.pkg %{driver_name}.pkg)

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Fri Feb 02 2024 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.11.17.1-2
- CA-386575: Fix enabling SR-IOV with Xen

* Mon Jul 31 2023 Stephen Cheng <stephen.cheng@citrix.com> - 1.11.17.1-1
- CP-41018: Update ice driver to 1.11.17.1; use auxiliary.ko in kernel

* Thu Feb 24 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.6.4-4
- CP-38416: Enable static analysis

* Mon Oct 18 2021 Igor Druzhinin <igor.druzhinin@citrix.com> - 1.6.4-3
- CP-32937: Move ice driver 1.6.4 to Koji

* Wed Jul 14 2021 Chuntian Xu <chuntian.xu@citrix.com> - 1.6.4-1
- CP-37345: Update ice driver to 1.6.4

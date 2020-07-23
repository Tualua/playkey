            #GIT_CMT=d1bcd3cda499cde97cab7d18c90e243f765cbf28
%ifarch %{ix86}
%global kvm_package         system-x86
%global have_x86_emul       1
%endif
%ifarch x86_64
%global kvm_package         system-x86
%global have_x86_emul       1
%endif
%ifarch aarch64
%global kvm_package         system-aarch64
%global have_aarch64_emul   1
%endif
%ifarch %{power64}
%global kvm_package         system-ppc
%endif
%ifarch s390x
%global kvm_package         system-s390x
%endif
%ifarch armv7hl
%global kvm_package         system-arm
%endif
%ifarch %{mips}
%global kvm_package         system-mips
%endif

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

# Support for the full set of QEMU instruction set emulators
%global have_user 0
%global have_all_emul 0

# Support for statically built versions of the emulators
%global user_static 0

# Generate documentation
%global have_docs 0

# Generate position-independent executables; note that disabling
# this makes it difficult to patch QEMU
%global have_pie 1

# Support for loadable modules
%global have_modules 0

# Debug switches
# Generate debug info
%global have_debug_info 0
# Debug the Tiny Code Generator
%global have_tcg_debug 0
# Debug casts
%global have_qom_cast_debug 0
# Enable Sparse semantic checker
%global have_sparse 0
# Mutex debugging support
%global have_debug_mutex 0

# Support for gperftools
%global have_gperftools 0

# Build qemu-io, qemu-nbd and qemu-image tools
%global have_tools 1

# Support for capstone disassembler
%global have_capstone 0

# qemu-kvm executable for backwards compatibility on x86
%global need_qemu_kvm 0

# Support for vnuma
%global have_numa 1

# Support curses on the HMP interface
%global have_curses 0

# Support for Linux AIO
%global have_linux_aio 1

# Support Linux's vhost-net module
%global have_vhost_net 1

# Support virtio sockets for host/guest communication
%global have_vhost_vsock 1

# Support vhost-crypto acceleration
%global have_vhost_crypto 0

# Support vhost-user
%global have_vhost_user 1

# Kernel Samepage Merging (KSM) support
%global have_ksm 0

# Support for replication
%global have_replication 1

# Support for xfsctl()
%global have_xfsctl 0

# Memory knobs
# Allocate a pool of memory for coroutines
%global have_coroutine_pool 1
# Thread-caching malloc
%global have_tcmalloc 0
# jemalloc
%global have_jemalloc 0
# membarrier system call (for Linux 4.14+ or Windows)
%global have_membarrier 0

# Security and capabilities checking knobs
# libseccomp
%global have_seccomp 1
# libattr
%global have_attr 1
# libcap-ng
%global have_libcapng 0

# Support for block storage backends
# iSCSI
%global have_iscsi 1
# Ceph/RBD
%global have_rbd 1
# GlusterFS
%global have_gluster 0
# VirtFS (required for Kata Containers)
%global have_virtfs 1
# NFS
%global have_nfs 0
# SSH
%global have_ssh 0
# Curl
%global have_curl 1
# MacOS DMG images
%global have_dmg 0
# Block migration in the main migration stream
%global have_live_block_migration 1

# Support for multipath persistent reservations
%global have_mpath 0

# Support for remote graphical consoles
# VNC
%global have_vnc 1
# SASL encryption for VNC
%global have_vnc_sasl 1
# JPEG compression for VNC
%global have_vnc_jpg 0
# PNG compression for VNC
%global have_vnc_png 0
# Spice
%global have_spice 0

# Support for compression libraries
# LZO
%global have_lzo 0
# Snappy
%global have_snappy 0
# bzip
%global have_bzip2 0

# Support for encryption libraries
# GNU TLS
%global have_gnutls 1
# Nettle
%global have_nettle 0
# libgrypt
%global have_gcrypt 0
# Linux AF_ALG crypto backend driver
%global have_crypto_afalg 1

# Miscellaneous networking support
# RDMA (for migration only)
%global have_rdma 0
# Virtual Distributed Ethernet (VDE)
%global have_vde 0
# netmap
%global have_netmap 0

# Support for miscellaneous hardware
# Trusted Platform Modules (TPM)
%global have_tpm 0
# Sound cards
%global have_audio 0
# USB redirection and passthrough
%global have_usb 1
# SmartCards
%global have_smartcard 0
# Bluetooth
%global have_bluetooth 0
# Braille
%global have_braille 0
# Flat Device Trees (required for ARM)
%if 0%{?have_aarch64_emul}
%global have_fdt 1
%else
%global have_fdt 0
%endif
# HAX acceleration support
%global have_hax 0
# Hypervisor.framework acceleration support
%global have_hvf 0
# Windows Hypervisor Platform acceleration support
%global have_whpx 0
# Veritas HyperScale vDisk backend support
%global have_vxhs 0

# Support for guest graphics APIs
# SDL/GTK
%global have_sdl_gtk 0
# OpenGL
%global have_opengl 0
# virgl
%global have_virgl 0

# Build guest agents for Linux and Windows
%global have_agent 0
%global have_windows_agent 0

# Xen is available only on i386/x86_64 (from libvirt spec)
%ifarch %{ix86} x86_64
%global have_xen 0
%endif

# Matches edk2.spec ExclusiveArch
# TODO: Revisit this after we finish packaging EDK2 for OCI.
%ifarch %{ix86} x86_64 %{arm} aarch64
%global have_edk2 0
%endif

# If we can run qemu-sanity-check, hostqemu gets defined.
%ifarch %{arm}
%global hostqemu arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
%global hostqemu arm-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
%global hostqemu i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
%global hostqemu x86_64-softmmu/qemu-system-x86_64
%endif

# QMP regdump tool (and sosreport plugin) is only supported on x86_64
%ifarch x86_64
%global have_qmpregdump 1
%endif

# Control whether to run Parfait static analysis on code base
%bcond_with parfait

# All block-* modules should be listed here.
%global requires_all_block_modules                               \
Requires: %{name}-block-curl = %{epoch}:%{version}-%{release}    \
Requires: %{name}-block-dmg = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-gluster = %{epoch}:%{version}-%{release} \
Requires: %{name}-block-iscsi = %{epoch}:%{version}-%{release}   \
Requires: %{name}-block-nfs = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-rbd = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-ssh = %{epoch}:%{version}-%{release}

# Temp hack for https://bugzilla.redhat.com/show_bug.cgi?id=1343892
# We'll manually turn on hardened build later in this spec
%undefine _hardened_build

# Release candidate version tracking
#global rcver rc4
#if 0%{?rcver:1}
#global rcrel .%{rcver}
#global rcstr -%{rcver}
#endif


Summary: QEMU is a FAST! processor emulator
Name: qemu
Version: 3.1.0
Release:    7.el7
Epoch: 15
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
Obsoletes: qemu-kvm-ev, qemu-img-ev, qemu-kvm-common-ev

Source0: qemu-3.1.0.tar.bz2

# Creates /dev/kvm
Source3: 80-kvm.rules

%if 0%{?have_ksm}
# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf
%endif

%if 0%{?have_agent}
# guest agent service
Source10: qemu-guest-agent.service
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
%endif

# /etc/qemu/bridge.conf
Source12: bridge.conf

%if 0%{?need_qemu_kvm}
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
%endif

# /etc/modprobe.d/kvm.conf
Source20: kvm.conf

%if 0%{?have_qmpregdump}
# /usr/bin/qmp-regdump
Source21: qmp-regdump
# /usr/lib/<python sitelib>/sos/plugins/qemu_regdump.py
Source22: qemu_regdump.py
%endif

# Parfait configuration file
Source23: parfait-qemu.conf

Patch0001: 0001-virtio-Set-PCI-subsystem-vendor-ID-to-Oracle.patch

# documentation deps
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl-podlators
# For sanity test
# BuildRequires: qemu-sanity-check-nodeps
# For acpi compilation
BuildRequires: iasl
# For chrpath calls in specfile
BuildRequires: chrpath

%if 0%{?have_sdl_gtk}
# -display sdl support
BuildRequires: SDL2-devel
%endif
# used in various places for compression
BuildRequires: zlib-devel
# used in various places for crypto
BuildRequires: gnutls-devel
# VNC sasl auth support
BuildRequires: cyrus-sasl-devel
# aio implementation for block drivers
BuildRequires: libaio-devel
%if 0%{?have_audio}
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# alsa audio output
BuildRequires: alsa-lib-devel
%endif
# qemu-pr-helper multipath support (requires libudev too)
%if 0%{?have_mpath}
BuildRequires: device-mapper-multipath-devel
%endif
BuildRequires: systemd-devel
%if 0%{?have_iscsi}
# iscsi drive support
%if 0%{?have_x86_emul}
BuildRequires: libiscsi-devel >= 1.9.0-8
%else
BuildRequires: libiscsi-devel
%endif
%endif
%if 0%{?have_nfs}
# NFS drive support
BuildRequires: libnfs-devel
%endif
%if 0%{?have_snappy}
# snappy compression for memory dump
BuildRequires: snappy-devel
%endif
%if 0%{?have_lzo}
# lzo compression for memory dump
BuildRequires: lzo-devel
%endif
%if 0%{?have_curses}
# needed for -display curses
BuildRequires: ncurses-devel
%endif
# used by 9pfs
%if 0%{?have_attr}
BuildRequires: libattr-devel
%endif
BuildRequires: libcap-devel
%if 0%{?have_libcapng}
# used by qemu-bridge-helper
BuildRequires: libcap-ng-devel
%endif
%if 0%{?have_spice}
# spice usb redirection support
BuildRequires: usbredir-devel >= 0.5.2
%endif
%ifnarch s390 s390x
%if 0%{?have_gperftools}
# tcmalloc support
BuildRequires: gperftools-devel
%endif
%endif
%if 0%{?have_spice:1}
# spice graphics support
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
%if 0%{?have_seccomp:1}
# seccomp containment support
BuildRequires: libseccomp-devel >= 2.3.0
%endif
%if 0%{?have_curl}
# For network block driver
BuildRequires: libcurl-devel
%endif
%if 0%{?have_rbd}
# For rbd block driver
BuildRequires: librbd1-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
%if 0%{?have_vnc_jpg}
# For VNC JPEG support
BuildRequires: libjpeg-devel
%endif
%if 0%{?have_vnc_png}
# For VNC PNG support
BuildRequires: libpng-devel
%endif
# For uuid generation
BuildRequires: libuuid-devel
%if 0%{?have_bluetooth}
# For BlueZ device support
BuildRequires: bluez-libs-devel
%endif
%if 0%{?have_braille}
# For Braille device support
BuildRequires: brlapi-devel
%endif
%if 0%{?have_fdt}
# For FDT device tree support
BuildRequires: libfdt-devel
%endif
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
%if 0%{?have_gluster}
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
%endif
%if 0%{?have_usb}
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
%endif
%if 0%{?have_ssh}
# SSH block driver
BuildRequires: libssh2-devel
%endif
%if 0%{?have_sdl_gtk}
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
# GTK translations
BuildRequires: gettext
%endif
# RDMA migration
%ifnarch s390 s390x
BuildRequires: librdmacm-devel
%endif
%if 0%{?have_xen}
# Xen support
BuildRequires: xen-devel
%endif
%ifarch %{ix86} x86_64 aarch64
# qemu 2.1: needed for memdev hostmem backend
BuildRequires: numactl-devel
%endif
# qemu 2.3: reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
%if 0%{?have_sdl_gtk}
# qemu 2.4: needed for opengl bits
BuildRequires: libepoxy-devel
%endif
# qemu 2.5: needed for TLS test suite
BuildRequires: libtasn1-devel
%if 0%{?have_smartcard}
# qemu 2.5: libcacard is it's own project now
BuildRequires: libcacard-devel >= 2.5.0
%endif
%if 0%{?have_virgl}
# qemu 2.5: virgl 3d support
BuildRequires: virglrenderer-devel
%endif
%if 0%{?have_sdl_gtk}
# qemu 2.6: Needed for gtk GL support
BuildRequires: mesa-libgbm-devel
%endif
%if 0%{?with_parfait}
# qemu 4.0: Needed for nproc(1)
BuildRequires: coreutils
%endif

# BuildRequires: glibc-static pcre-static glib2-static zlib-static

%if 0%{?hostqemu:1}
# For complicated reasons, this is required so that
# /bin/kernel-install puts the kernel directly into /boot, instead of
# into a /boot/<machine-id> subdirectory (in Fedora >= 23).  This is
# so we can run qemu-sanity-check.  Read the kernel-install script to
# understand why.
BuildRequires: grubby
%endif

%if 0%{?have_user}
Requires: %{name}-user = %{epoch}:%{version}-%{release}
%endif
%if 0%{?have_all_emul}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-lm32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or1k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-unicore32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-system-moxie = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-system-nios2 = %{epoch}:%{version}-%{release}
%endif
%if 0%{?have_x86_emul}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
%endif
%if 0%{?have_aarch64_emul}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
%endif
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.


%package  common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires: ipxe-roms-qemu
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description common
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets

%if 0%{?have_ksm}
%package -n ksm
Summary: Kernel Samepage Merging services
Group: Development/Tools
Requires(post): systemd-units
Requires(postun): systemd-units
%description -n ksm
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling and tuning KSM.
%endif

%if 0%{?have_agent}
%package guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description guest-agent
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.
%endif

%package  img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description img
This package provides a command line tool for manipulating disk images

%if 0%{?have_curl}
%package  block-curl
Summary: QEMU CURL block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.
%endif

%if 0%{?have_dmg}
%package  block-dmg
Summary: QEMU block driver for DMG disk images
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.
%endif

%if 0%{?have_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif

%if 0%{?have_iscsi}
%package  block-iscsi
Summary: QEMU iSCSI block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.
%endif

%if 0%{?have_nfs}
%package  block-nfs
Summary: QEMU NFS block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif

%if 0%{?have_rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%if 0%{?have_ssh}
%package  block-ssh
Summary: QEMU SSH block driver
Group: Development/Tools
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.
%endif

%package -n ivshmem-tools
Summary: Client and server for QEMU ivshmem device
Group: Development/Tools

%description -n ivshmem-tools
This package provides client and server tools for QEMU's ivshmem device.


%if 0%{?have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-kvm-common, %{name}-kvm-tools

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Group: Development/Tools
Requires: qemu-%{kvm_package}-core = %{epoch}:%{version}-%{release}

%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif

%if 0%{?have_user}
%package user
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}

%description user
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets
%endif

%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Group: Development/Tools
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-static
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}

%description user-binfmt
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-binfmt
Provides: %{name}-user-binfmt

%description user-static
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the user mode emulation of qemu targets built as
static binaries
%endif


%package system-x86
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-system-x86-core = %{epoch}:%{version}-%{release}

%description system-x86
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-x86-core
Summary: QEMU system emulator for x86
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: seabios-bin >= 1.10.2-4
Requires: sgabios-bin
Requires: seavgabios-bin >= 1.10.2-4
%if 0%{?have_edk2}
Requires: edk2-ovmf
%endif
%if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
%endif


%description system-x86-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-aarch64
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-system-aarch64-core = %{epoch}:%{version}-%{release}
%description system-aarch64
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%if 0%{?have_edk2:1}
Requires: AAVMF
%endif
%description system-aarch64-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for AArch64.

%if 0%{?have_all_emul}
%package system-alpha
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-system-alpha-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-alpha
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-alpha-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-system-arm-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-arm
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ARM boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-system-mips-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-mips
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for MIPS boards.


%package system-cris
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-system-cris-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-cris
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for CRIS boards.


%package system-lm32
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-system-lm32-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-lm32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 systems.

%package system-lm32-core
Summary: QEMU system emulator for LatticeMico32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-lm32-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for LatticeMico32 boards.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-system-m68k-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-m68k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-system-microblaze-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-microblaze-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Microblaze boards.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-system-or1k-core = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32 < 2:2.9.0
%{requires_all_block_modules}
%description system-or1k
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32-core < 2:2.9.0
%description system-or1k-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for OpenRisc32 boards.


%package system-s390x
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-system-s390x-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-s390x
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-s390x-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-system-sh4-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-sh4
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-system-sparc-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-sparc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.

%package system-sparc-core
Summary: QEMU system emulator for SPARC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description system-sparc-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for SPARC and SPARC64 systems.


%package system-ppc
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-system-ppc-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-ppc
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
Requires: seavgabios-bin
%description system-ppc-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for PPC and PPC64 systems.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-system-xtensa-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-xtensa-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Xtensa boards.


%package system-unicore32
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-system-unicore32-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-unicore32
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.

%package system-unicore32-core
Summary: QEMU system emulator for Unicore32
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-unicore32-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Unicore32 boards.


%package system-moxie
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-system-moxie-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-moxie
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.

%package system-moxie-core
Summary: QEMU system emulator for Moxie
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-moxie-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Moxie boards.

%package system-tricore
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-system-tricore-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-tricore
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-tricore-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for Tricore.


%package system-nios2
Summary: QEMU system emulator for nios2
Group: Development/Tools
Requires: %{name}-system-nios2-core = %{epoch}:%{version}-%{release}
%{requires_all_block_modules}
%description system-nios2
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Group: Development/Tools
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-nios2-core
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation.

This package provides the system emulator for NIOS2.
%endif


%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1


%build

# QEMU already knows how to set _FORTIFY_SOURCE
%global optflags %(echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

# drop -g flag to prevent memory exhaustion by linker
%ifarch s390
%global optflags %(echo %{optflags} | sed 's/-g//')
sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
%global _smp_mflags %{nil}
%endif


# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

%if 0%{?have_x86_emul}
    system_arch="$system_arch i386 x86_64"
%endif
%if 0%{?have_aarch64_emul}
    system_arch="aarch64"
%endif
%if 0%{?have_all_emul}
    system_arch="\
        aarch64 \
        alpha \
        arm \
        cris \
        lm32 \
        m68k \
        microblaze \
        microblazeel \
        mips \
        mips64 \
        mips64el \
        mipsel \
        moxie \
        nios2 \
        or1k \
        ppc \
        ppc64 \
        ppcemb \
        s390x \
        sh4 \
        sh4eb \
        sparc \
        sparc64 \
        tricore \
        unicore32 \
        xtensa \
        xtensaeb"
%endif

%if 0%{?have_user}
    user_arch="\
        aarch64 \
        alpha \
        arm \
        armeb \
        cris \
        i386 \
        hppa \
        m68k \
        microblaze \
        microblazeel \
        mips \
        mips64 \
        mips64el \
        mipsel \
        mipsn32 \
        mipsn32el \
        nios2 \
        or1k \
        ppc \
        ppc64 \
        ppc64abi32 \
        ppc64le \
        s390x \
        sh4 \
        sh4eb \
        sparc \
        sparc32plus \
        sparc64 \
        x86_64"
%endif

dynamic_targets=
static_targets=

for arch in $system_arch
do
  dynamic_targets="$dynamic_targets $arch-softmmu"
done

for arch in $user_arch
do
  dynamic_targets="$dynamic_targets $arch-linux-user"
  static_targets="$static_targets $arch-linux-user"
done


%if 0%{?have_spice}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif

%if 0%{?have_iscsi}
    %global iscsiflag --enable-libiscsi
%else
    %global iscsiflag --disable-libiscsi
%endif

%if 0%{?have_smartcard}
    %global smartcardflag --enable-smartcard
%else
    %global smartcardflag --disable-smartcard
%endif

%if 0%{?have_fdt}
    %global fdtflag --enable-fdt
%else
    %global fdtflag --disable-fdt
%endif

%if 0%{?have_rbd}
    %global rbdflag --enable-rbd
%else
    %global rbdflag --disable-rbd
%endif

%if 0%{?have_sdl_gtk}
    %global sdlflag --enable-sdl --enable-virglrenderer --enable-gtk --enable-vte
%else
    %global sdlflag --disable-sdl --disable-virglrenderer --disable-gtk --disable-vte
%endif

%if 0%{?have_audio}
    %global audioflags --audio-drv-list=pa,sdl,alsa,oss
%else
    %global audioflags --audio-drv-list=""
%endif

%if 0%{?have_agent}
    %global guestflags --enable-guest-agent
%else
    %global guestflags --disable-guest-agent
%endif

%if 0%{?have_windows_agent}
    %global windowsguestflags --enable-guest-agent-msi
%else
    %global windowsguestflags --disable-guest-agent-msi
%endif

%if 0%{?have_tpm}
    %global tpmflags --enable-tpm
%else
    %global tpmflags --disable-tpm
%endif

%if 0%{?have_user}
    %global userflags --enable-user --enable-linux-user --disable-bsd-user
%else
    %global userflags --disable-user --disable-linux-user --disable-bsd-user
%endif

%if 0%{?have_docs}
    %global docsflags --enable-docs
%else
    %global docsflags --disable-docs
%endif

%if 0%{?have_pie}
    %global pieflags --enable-pie
%else
    %global pieflags --disable-pie
%endif

%if 0%{?have_modules}
    %global moduleflags --enable-modules
%else
    %global moduleflags --disable-modules
%endif

%if 0%{?have_tcg_debug}
    %global tcgdebugflags --enable-debug-tcg
%else
    %global tcgdebugflags --disable-debug-tcg
%endif

%if 0%{?have_debug_info}
    %global debuginfoflags --enable-debug-info
%else
    %global debuginfoflags --disable-debug-info
%endif

%if 0%{?have_sparse}
    %global sparseflags --enable-sparse
%else
    %global sparseflags --disable-sparse
%endif

%if 0%{?have_gnutls}
    %global gnutlsflags --enable-gnutls
%else
    %global gnutlsflags --disable-gnutls
%endif

%if 0%{?have_nettle}
    %global nettleflags --enable-nettle
%else
    %global nettleflags --disable-nettle
%endif

%if 0%{?have_gcrypt}
    %global gcryptflags --enable-gcrypt
%else
    %global gcryptflags --disable-gcrypt
%endif

%if 0%{?have_curses}
    %global cursesflags --enable-curses
%else
    %global cursesflags --disable-curses
%endif

%if 0%{?have_vnc}
    %global vncflags --enable-vnc
%else
    %global vncflags --disable-vnc
%endif

%if 0%{?have_vnc_sasl}
    %global vncsaslflags --enable-vnc-sasl
%else
    %global vncsaslflags --disable-vnc-sasl
%endif

%if 0%{?have_vnc_jpg}
    %global vncjpgflags --enable-vnc-jpeg
%else
    %global vncjpgflags --disable-vnc-jpeg
%endif

%if 0%{?have_vnc_png}
    %global vncpngflags --enable-vnc-png
%else
    %global vncpngflags --disable-vnc-png
%endif

%if 0%{?have_virtfs}
    %global virtfsflags --enable-virtfs
%else
    %global virtfsflags --disable-virtfs
%endif

%if 0%{?have_braille}
    %global brailleflags --enable-brlapi
%else
    %global brailleflags --disable-brlapi
%endif

%if 0%{?have_xen}
    %global xenflags --enable-xen --enable-xen-pci-passthrough
%else
    %global xenflags --disable-xen --disable-xen-pci-passthrough
%endif

%if 0%{?have_curl}
    %global curlflags --enable-curl
%else
    %global curlflags --disable-curl
%endif

%if 0%{?have_bluetooth}
    %global bluetoothflags --enable-bluez
%else
    %global bluetoothflags --disable-bluez
%endif

%if 0%{?have_rdma}
    %global rdmaflags --enable-rdma
%else
    %global rdmaflags --disable-rdma
%endif

%if 0%{?have_vde}
    %global vdeflags --enable-vde
%else
    %global vdeflags --disable-vde
%endif

%if 0%{?have_netmap}
    %global netmapflags --enable-netmap
%else
    %global netmapflags --disable-netmap
%endif

%if 0%{?have_linux_aio}
    %global linuxaioflags --enable-linux-aio
%else
    %global linuxaioflags --disable-linux-aio
%endif

%if 0%{?have_libcapng}
    %global libcapngflags --enable-cap-ng
%else
    %global libcapngflags --disable-cap-ng
%endif

%if 0%{?have_attr}
    %global attrflags --enable-attr
%else
    %global attrflags --disable-attr
%endif

%if 0%{?have_vhost_net}
    %global vhostnetflags --enable-vhost-net
%else
    %global vhostnetflags --disable-vhost-net
%endif

%if 0%{?have_nfs}
    %global nfsflags --enable-libnfs
%else
    %global nfsflags --disable-libnfs
%endif

%if 0%{?have_usb}
    %global usbflags --enable-libusb --enable-usb-redir
%else
    %global usbflags --disable-libusb --disable-usb-redir
%endif

%if 0%{?have_lzo}
    %global lzoflags --enable-lzo
%else
    %global lzoflags --disable-lzo
%endif

%if 0%{?have_snappy}
    %global snappyflags --enable-snappy
%else
    %global snappyflags --disable-snappy
%endif

%if 0%{?have_bzip2}
    %global bzip2flags --enable-bzip2
%else
    %global bzip2flags --disable-bzip2
%endif

%if 0%{?have_seccomp}
    %global seccompflags --enable-seccomp
%else
    %global seccompflags --disable-seccomp
%endif

%if 0%{?have_coroutine_pool}
    %global coroutineflags --enable-coroutine-pool
%else
    %global coroutineflags --disable-coroutine-pool
%endif

%if 0%{?have_gluster}
    %global glusterflags --enable-glusterfs
%else
    %global glusterflags --disable-glusterfs
%endif

%if 0%{?have_ssh}
    %global sshflags --enable-libssh2
%else
    %global sshflags --disable-libssh2
%endif

%if 0%{?have_numa}
    %global numaflags --enable-numa
%else
    %global numaflags --disable-numa
%endif

%if 0%{?have_tcmalloc}
    %global tcmallocflags --enable-tcmalloc
%else
    %global tcmallocflags --disable-tcmalloc
%endif

%if 0%{?have_jemalloc}
    %global jemallocflags --enable-jemalloc
%else
    %global jemallocflags --disable-jemalloc
%endif

%if 0%{?have_replication}
    %global replicationflags --enable-replication
%else
    %global replicationflags --disable-replication
%endif

%if 0%{?have_vhost_vsock}
    %global vhostvsockflags --enable-vhost-vsock
%else
    %global vhostvsockflags --disable-vhost-vsock
%endif

%if 0%{?have_opengl}
    %global openglflags --enable-opengl
%else
    %global openglflags --disable-opengl
%endif

%if 0%{?have_virgl}
    %global virglflags --enable-virglrenderer
%else
    %global virglflags --disable-virglrenderer
%endif

%if 0%{?have_xfsctl}
    %global xfsctlflags --enable-xfsctl
%else
    %global xfsctlflags --disable-xfsctl
%endif

%if 0%{?have_mpath}
    %global mpathflags --enable-mpath
%else
    %global mpathflags --disable-mpath
%endif

%if 0%{?have_capstone}
    %global capstoneflags --enable-capstone
%else
    %global capstoneflags --disable-capstone
%endif

%if 0%{?have_qom_cast_debug}
    %global qomcastflags --enable-qom-cast-debug
%else
    %global qomcastflags --disable-qom-cast-debug
%endif

%if 0%{?have_membarrier}
    %global membarrierflags --enable-membarrier
%else
    %global membarrierflags --disable-membarrier
%endif

%if 0%{?have_hax}
    %global haxflags --enable-hax
%else
    %global haxflags --disable-hax
%endif

%if 0%{?have_hvf}
    %global hvfflags --enable-hvf
%else
    %global hvfflags --disable-hvf
%endif

%if 0%{?have_whpx}
    %global whpxflags --enable-whpx
%else
    %global whpxflags --disable-whpx
%endif

%if 0%{?have_vhost_crypto}
    %global vhostcyptoflags --enable-vhost-crypto
%else
    %global vhostcyptoflags --disable-vhost-crypto
%endif

%if 0%{?have_live_block_migration}
    %global liveblockmigrationflags --enable-live-block-migration
%else
    %global liveblockmigrationflags --disable-live-block-migration
%endif

%if 0%{?have_tools}
    %global toolsflags --enable-tools
%else
    %global toolsflags --disable-tools
%endif

%if 0%{?have_crypto_afalg}
    %global cryptoafalgflags --enable-crypto-afalg
%else
    %global cryptoafalgflags --disable-crypto-afalg
%endif

%if 0%{?have_vhost_user}
    %global vhostuserflags --enable-vhost-user
%else
    %global vhostuserflags --disable-vhost-user
%endif

%if 0%{?have_debug_mutex}
    %global debugmutexflags --enable-debug-mutex
%else
    %global debugmutexflags --disable-debug-mutex
%endif

%if 0%{?have_vxhs}
    %global vxhsflags --enable-vxhs
%else
    %global vxhsflags --disable-vxhs
%endif

run_configure() {
    ../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --disable-strip \
        --enable-werror \
        --enable-kvm \
%ifarch s390 %{mips64}
        --enable-tcg-interpreter \
%endif
        --enable-trace-backend=$tracebackends \
	%{?with_parfait:--disable-avx2} \
	%{?with_parfait:--cc=parfait-gcc} \
	%{?with_parfait:--cxx=parfait-g++} \
	%{?with_parfait:--extra-cflags="-B parfait-ld"} \
        %{spiceflag} \
        %{iscsiflag} \
        %{smartcardflag} \
        %{fdtflag} \
        %{rbdflag} \
        %{sdlflag} \
        %{audioflags} \
        --with-sdlabi="2.0" \
        %{guestflags} \
        %{windowsguestflags} \
        %{tpmflags} \
        %{userflags} \
        %{docsflags} \
        %{pieflags} \
        %{moduleflags} \
        %{tcgdebugflags} \
        %{debuginfoflags} \
        %{sparseflags} \
        %{gnutlsflags} \
        %{nettleflags} \
        %{gcryptflags} \
        %{cursesflags} \
        %{vncflags} \
        %{vncsaslflags} \
        %{vncjpgflags} \
        %{vncpngflags} \
        %{virtfsflags} \
        %{xenflags} \
        %{brailleflags} \
        %{curlflags} \
        %{bluetoothflags} \
        %{rdmaflags} \
        %{vdeflags} \
        %{netmapflags} \
        %{linuxaioflags} \
        %{libcapngflags} \
        %{attrflags} \
        %{vhostnetflags} \
        %{nfsflags} \
        %{usbflags} \
        %{lzoflags} \
        %{snappyflags} \
        %{bzip2flags} \
        %{seccompflags} \
        %{coroutineflags} \
        %{glusterflags} \
        %{sshflags} \
        %{numaflags} \
        %{tcmallocflags} \
        %{jemallocflags} \
        %{replicationflags} \
        %{vhostvsockflags} \
        %{openglflags} \
        %{virglflags} \
        %{xfsctlflags} \
        %{qomcastflags} \
        %{mpathflags} \
        %{capstoneflags} \
        %{membarrierflags} \
        %{haxflags} \
        %{hvfflags} \
        %{whpxflags} \
        %{vhostcyptoflags} \
        %{liveblockmigrationflags} \
        %{toolsflags} \
        %{cryptoafalgflags} \
        %{vhostuserflags} \
        %{debugmutexflags} \
        %{vxhsflags} \
        "$@" || cat config.log
}

mkdir build-dynamic
pushd build-dynamic

run_configure \
%ifnarch aarch64
    --extra-ldflags="$extraldflags -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -pie -Wl,-z,relro -Wl,-z,now" \
%else
    --extra-ldflags="$extraldflags -specs=/usr/lib/rpm/redhat/redhat-hardened-ld" \
%endif
    --extra-cflags="%{optflags} -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1" \
    --target-list="$dynamic_targets" \
    --enable-pie \
    --enable-modules \
    --tls-priority=@QEMU,SYSTEM \
    %{spiceflag} \
    --with-sdlabi="2.0"

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

popd

%if 0%{?user_static}
mkdir build-static
pushd build-static

run_configure \
%ifnarch aarch64
    --extra-ldflags="$extraldflags -Wl,-z,relro -Wl,-z,now" \
%else
    --extra-ldflags="$extraldflags" \
%endif
    --extra-cflags="%{optflags}" \
    --target-list="$static_targets" \
    --static \
    --disable-pie \
    --disable-tcmalloc \
    --disable-sdl \
    --disable-gtk \
    --disable-spice \
    --disable-tools \
    --disable-guest-agent \
    --disable-guest-agent-msi \
    --disable-curses \
    --disable-curl \
    --disable-gnutls \
    --disable-gcrypt \
    --disable-nettle \
    --disable-cap-ng \
    --disable-brlapi \
    --disable-libnfs \
    --disable-vnc-sasl

make V=1 %{?_smp_mflags} $buildldflags

popd
%endif

# gcc %{_sourcedir}/ksmctl.c -O2 -g -o ksmctl

#
# Run Parfait static analysis tool against specified baseline
# if '--with parfait' is passed to rpmbuild.
#
# http://parfait.us.oracle.com/
#
%if %{with parfait}
# URL to use for Parfait baseline
_parfait_server=%{?_parfait_server}%{!?_parfait_server:http://ca-qa-parfait.us.oracle.com:9990/parfait-server/projects/QEMU/tasks/v%{version}}
# number of jobs to run in parallel (default: value returned by nproc(1).)
_parfait_threads=%{?_parfait_threads}%{!?_parfait_threads:$(nproc)}
# Location to store graphical report (default: ./parfait_html in BUILD dir)
_parfait_output=%{?_parfait_output}%{!?_parfait_output:"./parfait_html"}
# Location of Parfait configuration rules file
_parfait_conf=%{_sourcedir}/parfait-qemu.conf
#
# Select whether to compare against baseline (default) using '-b'
# or upload results (-s) if _parfait_upload is set to 1 on command-line
# (if _parfait_upload is set, the the source base dir is also set via -z)
#
_parfait_upload=%{?_parfait_upload:"-s"}%{!?_parfait_upload:"-b"}
_parfait_srcdir=%{?_parfait_upload:"-z %{_builddir}/%{name}-%{version}/"}

RC=0
parfait -j $_parfait_threads -c $_parfait_conf -g $_parfait_output $_parfait_upload $_parfait_server $_parfait_srcdir . || RC=$?

#
# Work is ongoing to triage all the issues reported by Parfait on the QEMU
# codebase but until they are all are either fixed or marked as a
# False Positive/Will-Not-Fix on the QEMU Parfait server ($_parfait_server),
# the parfait run will return 1 so we need to check the return value
# and ignore it if it's 1 or zero (success, in which case this check can be
# removed).
#
# For more details on exit codes, see the Parfait documentation:
# http://parfait.us.oracle.com/latest/ParfaitInfo.html#exit-codes
#
if [ ${RC} != 0 -a ${RC} != 1 ]; then
    exit ${RC}
fi
%endif	# with parfait

%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/%{name}

mkdir -p %{buildroot}%{_udevdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/qemu

%if 0%{?have_ksm}
install -D -p -m 0644 %{_sourcedir}/ksm.service %{buildroot}%{_unitdir}
install -D -p -m 0644 %{_sourcedir}/ksm.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl %{buildroot}%{_libexecdir}/ksmctl

install -D -p -m 0644 %{_sourcedir}/ksmtuned.service %{buildroot}%{_unitdir}
install -D -p -m 0755 %{_sourcedir}/ksmtuned %{buildroot}%{_sbindir}/ksmtuned
install -D -p -m 0644 %{_sourcedir}/ksmtuned.conf %{buildroot}%{_sysconfdir}/ksmtuned.conf
%endif

install -D -p -m 0644 %{_sourcedir}/kvm.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf

%if 0%{?have_agent}
# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}
%endif

%ifarch s390x
install -d %{buildroot}%{_sysconfdir}/sysctl.d
install -m 0644 %{_sourcedir}/50-kvm-s390x.conf %{buildroot}%{_sysconfdir}/sysctl.d
%endif

%ifarch %{power64}
install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -m 0644 %{_sourcedir}/95-kvm-ppc64-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d
%endif

# Install kvm specific bits
%if 0%{?have_kvm}
mkdir -p %{buildroot}%{_bindir}/
install -m 0644 %{_sourcedir}/80-kvm.rules %{buildroot}%{_udevdir}
%endif

%if %{user_static}
pushd build-static
make DESTDIR=%{buildroot} install

# Give all QEMU user emulators a -static suffix
for src in %{buildroot}%{_bindir}/qemu-*
do
  mv $src $src-static
done

# Update trace files to match

for src in %{buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp
do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
done

popd
%endif

pushd build-dynamic
make DESTDIR=%{buildroot} install
popd

%if 0%{?have_sdl_gtk}
%find_lang %{name}
%endif

%if 0%{?have_docs}
chmod -x %{buildroot}%{_mandir}/man1/*
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README COPYING COPYING.LIB LICENSE
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done
%endif

%if 0%{?need_qemu_kvm}
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
%endif

install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
# TODO: Revisit %{buildroot}%{_datadir}/%{name}/efi*rom files
# after we finish packaging EDK2 for BMCS.
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# We don't package the setuid root qemu-bridge-helper script
rm -rf %{buildroot}%{_libexecdir}/qemu-bridge-helper

%if 0%{?have_all_emul}
%else
unused_blobs="QEMU,cgthree.bin QEMU,tcx.bin bamboo.dtb palcode-clipper \
petalogix-ml605.dtb petalogix-s3adsp1800.dtb ppc_rom.bin \
s390-ccw.img s390-zipl.rom spapr-rtas.bin u-boot.e500 \
skiboot.lid qemu_vga.ndrv s390-netboot.img canyonlands.dtb \
hppa-firmware.img u-boot-sam460-20100605.bin"
for blob in $unused_blobs; do
   rm -rf %{buildroot}%{_datadir}/%{name}/$blob
done

rm -rf %{buildroot}%{_bindir}/qemu-edid
rm -rf %{buildroot}%{_bindir}/qemu-keymap

%endif

# TODO: Revisit this after we finish packaging EDK2 and ipxe
# for BMCS.
pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
pxe_link eepro100 80861209
pxe_link e1000e 808610d3
pxe_link vmxnet3 15ad07b0

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../sgabios/sgabios.bin sgabios.bin

%if 0%{?have_user}
# Install binfmt
mkdir -p %{buildroot}%{_exec_prefix}/lib/binfmt.d
for i in dummy \
%ifnarch %{ix86} x86_64
    qemu-i386 \
%endif
%ifnarch alpha
    qemu-alpha \
%endif
%ifnarch aarch64
    qemu-aarch64 \
%endif
%ifnarch %{arm}
    qemu-arm \
%endif
    qemu-armeb \
    qemu-cris \
    qemu-microblaze qemu-microblazeel \
%ifnarch mips64
    qemu-mips64 \
%ifnarch mips
    qemu-mips \
%endif
%endif
%ifnarch mips64el
    qemu-mips64el \
%ifnarch mipsel
    qemu-mipsel \
%endif
%endif
%ifnarch m68k
    qemu-m68k \
%endif
%ifnarch ppc %{power64}
    qemu-ppc qemu-ppc64abi32 qemu-ppc64 \
%endif
%ifnarch sparc sparc64
    qemu-sparc qemu-sparc32plus qemu-sparc64 \
%endif
%ifnarch s390 s390x
    qemu-s390x \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
    qemu-sh4eb \
; do
  test $i = dummy && continue

  grep /$i:\$ %{_sourcedir}/qemu.binfmt > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-dynamic.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-dynamic.conf

%if %{user_static}
  grep /$i:\$ %{_sourcedir}/qemu.binfmt | tr -d '\n' > %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  echo "F" >> %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  perl -i -p -e "s/$i:F/$i-static:F/" %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
  chmod 644 %{buildroot}%{_exec_prefix}/lib/binfmt.d/$i-static.conf
%endif

done < %{_sourcedir}/qemu.binfmt
%endif


# Install rules to use the bridge helper with libvirt's virbr0
install -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu

%if 0%{?have_qmpregdump}
# Install in /usr/bin
install -m 0755 %{_sourcedir}/qmp-regdump %{buildroot}%{_bindir}/
# Install in /usr/lib/<python sitelib>/sos/plugins/
mkdir -p %{buildroot}%{python_sitelib}/sos/plugins
install -m 0755 %{_sourcedir}/qemu_regdump.py %{buildroot}%{python_sitelib}/sos/plugins
%endif

# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF | grep -q -i shared; then chrpath --delete $f; fi
done

# We need to make the block device modules executable else
# RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/block-*.so


%check

# Tests are hanging on s390 as of 2.3.0
#   https://bugzilla.redhat.com/show_bug.cgi?id=1206057
# Tests seem to be a recurring problem on s390, so I'd suggest just leaving
# it disabled.
%global archs_skip_tests s390
%global archs_ignore_test_failures 0

pushd build-dynamic
%ifnarch %{archs_skip_tests}

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%ifarch %{archs_ignore_test_failures}
make check V=1
%else
make check V=1 || :
%endif

# %if 0%{?hostqemu:1}
# Sanity-check current kernel can boot on this qemu.
# The results are advisory only.
# qemu-sanity-check --qemu=%{?hostqemu} ||:
# %endif

%endif  # archs_skip_tests
popd


%if 0%{?have_kvm}
%post %{kvm_package}
# Default /dev/kvm permissions are 660, we install a udev rule changing that
# to 666. However trying to trigger the re-permissioning via udev has been
# a neverending source of trouble, so we just force it with chmod. For
# more info see: https://bugzilla.redhat.com/show_bug.cgi?id=950436
chmod --quiet 666 /dev/kvm || :

%ifarch s390x
%sysctl_apply 50-kvm-s390x.conf
%endif
%endif

%post system-x86-core
%if 0%{?have_kvm}
udevadm control --reload >/dev/null 2>&1 || :
udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
chmod --quiet 666 /dev/kvm || :
%endif

%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu


%if 0%{?have_ksm}
%post -n ksm
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun -n ksm
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun -n ksm
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service
%endif

%if 0%{?have_user}
%post user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%if 0%{?have_agent}
%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service
%endif


%global kvm_files \
%{_udevdir}/80-kvm.rules

%files
# Deliberately empty

%if 0%{?have_sdl_gtk}
%files common -f %{name}.lang
%else
%files common
%endif
%if 0%{?have_docs}
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-doc.txt
%doc %{qemudocdir}/qemu-ga-ref.html
%doc %{qemudocdir}/qemu-ga-ref.txt
%doc %{qemudocdir}/qemu-qmp-ref.html
%doc %{qemudocdir}/qemu-qmp-ref.txt
%doc %{qemudocdir}/README
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%endif
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events-all
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-e1000e.rom
%{_datadir}/%{name}/efi-e1000e.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-vmxnet3.rom
%{_datadir}/%{name}/efi-vmxnet3.rom
%if 0%{?have_virtfs}
%{_bindir}/virtfs-proxy-helper
%endif
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%dir %{_libdir}/qemu
%if 0%{?have_qmpregdump}
%config(noreplace) %{_bindir}/qmp-regdump
%config(noreplace) %{python_sitelib}/sos/plugins/qemu_regdump.py*
%endif

%if 0%{?have_ksm}
%files -n ksm
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%endif

%if 0%{?have_agent}
%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%endif

%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%if 0%{?have_docs}
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%endif

%if 0%{?have_curl}
%files block-curl
%{_libdir}/qemu/block-curl.so
%endif

%if 0%{?have_dmg}
%files block-dmg
%{_libdir}/qemu/block-dmg-bz2.so
%endif

%if 0%{?have_gluster}
%files block-gluster
%{_libdir}/qemu/block-gluster.so
%endif

%if 0%{?have_iscsi}
%files block-iscsi
%{_libdir}/qemu/block-iscsi.so
%endif

%if 0%{?have_nfs}
%files block-nfs
%{_libdir}/qemu/block-nfs.so
%endif

%if 0%{?have_rbd}
%files block-rbd
%{_libdir}/qemu/block-rbd.so
%endif

%if 0%{?have_ssh}
%files block-ssh
%{_libdir}/qemu/block-ssh.so
%endif

%files -n ivshmem-tools
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif

%if 0%{?have_user}
%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64

%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-aarch64.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-cris.stp
%{_datadir}/systemtap/tapset/qemu-cris-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hppa.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-nios2.stp
%{_datadir}/systemtap/tapset/qemu-nios2-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-or1k.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace.stp

%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static
%{_exec_prefix}/lib/binfmt.d/qemu-*-static.conf
%{_bindir}/qemu-i386-static
%{_bindir}/qemu-x86_64-static
%{_bindir}/qemu-aarch64-static
%{_bindir}/qemu-alpha-static
%{_bindir}/qemu-arm-static
%{_bindir}/qemu-armeb-static
%{_bindir}/qemu-cris-static
%{_bindir}/qemu-hppa-static
%{_bindir}/qemu-m68k-static
%{_bindir}/qemu-microblaze-static
%{_bindir}/qemu-microblazeel-static
%{_bindir}/qemu-mips-static
%{_bindir}/qemu-mipsel-static
%{_bindir}/qemu-mips64-static
%{_bindir}/qemu-mips64el-static
%{_bindir}/qemu-mipsn32-static
%{_bindir}/qemu-mipsn32el-static
%{_bindir}/qemu-nios2-static
%{_bindir}/qemu-or1k-static
%{_bindir}/qemu-ppc-static
%{_bindir}/qemu-ppc64-static
%{_bindir}/qemu-ppc64abi32-static
%{_bindir}/qemu-ppc64le-static
%{_bindir}/qemu-s390x-static
%{_bindir}/qemu-sh4-static
%{_bindir}/qemu-sh4eb-static
%{_bindir}/qemu-sparc-static
%{_bindir}/qemu-sparc32plus-static
%{_bindir}/qemu-sparc64-static

%{_datadir}/systemtap/tapset/qemu-i386-static.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-cris-static.stp
%{_datadir}/systemtap/tapset/qemu-cris-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-nios2-static.stp
%{_datadir}/systemtap/tapset/qemu-nios2-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64abi32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace-static.stp
%endif
%endif

%if 0%{?have_x86_emul}
%files system-x86
# Deliberately empty

%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_bindir}/qemu-pr-helper
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{?kvm_files:}
%if 0%{?have_docs}
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%endif
%endif


%if 0%{?have_aarch64_emul}
%files system-aarch64
# Deliberately empty

%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_bindir}/qemu-pr-helper
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{?kvm_files:}
%if 0%{?have_docs}
%{_mandir}/man1/qemu-system-aarch64.1*
%endif
%endif

%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif

%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/sgabios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/kvmvapic.bin
%ifarch %{ix86} x86_64
%{?kvm_files:}
%endif


%if 0%{?have_all_emul}
%files system-alpha
# Deliberately empty

%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
# Deliberately empty

%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*
%ifarch armv7hl
%{?kvm_files:}
%endif


%files system-mips
# Deliberately empty

%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*
%ifarch %{mips}
%{?kvm_files:}
%endif


%files system-cris
# Deliberately empty

%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-lm32
# Deliberately empty

%files system-lm32-core
%{_bindir}/qemu-system-lm32
%{_datadir}/systemtap/tapset/qemu-system-lm32*.stp
%{_mandir}/man1/qemu-system-lm32.1*


%files system-m68k
# Deliberately empty

%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
# Deliberately empty

%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-or1k
# Deliberately empty

%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-s390x
# Deliberately empty

%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%ifarch s390x
%{?kvm_files:}
%{_sysconfdir}/sysctl.d/50-kvm-s390x.conf
%endif


%files system-sh4
# Deliberately empty

%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
# Deliberately empty

%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-ppc
# Deliberately empty

%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_bindir}/qemu-system-ppcemb
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_mandir}/man1/qemu-system-ppcemb.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/ppc_rom.bin
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/spapr-rtas.bin
%{_datadir}/%{name}/u-boot.e500
%ifarch %{power64}
%{?kvm_files:}
%{_sysconfdir}/security/limits.d/95-kvm-ppc64-memlock.conf
%endif


%files system-unicore32
# Deliberately empty

%files system-unicore32-core
%{_bindir}/qemu-system-unicore32
%{_datadir}/systemtap/tapset/qemu-system-unicore32*.stp
%{_mandir}/man1/qemu-system-unicore32.1*


%files system-xtensa
# Deliberately empty

%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%files system-moxie
# Deliberately empty

%files system-moxie-core
%{_bindir}/qemu-system-moxie
%{_datadir}/systemtap/tapset/qemu-system-moxie*.stp
%{_mandir}/man1/qemu-system-moxie.1*


%files system-tricore
# Deliberately empty

%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-nios2
# Deliberately empty

%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*
%endif


%changelog
* Wed Mar 4 2020 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-7.el7
- qemu-img: Add --target-is-zero to convert (David Edmondson)

* Thu Feb 06 2020 Karl Heubaum <karl.heubaum@oracle.com> - 15:3.1.0-6.el7
- qemu.spec: Remove "BuildRequires: kernel" (Karl Heubaum)  [Orabug: 30858754] 
- target/i386: add support for MSR_IA32_TSX_CTRL (Paolo Bonzini)  [Orabug: 30652327] 
- iscsi: Cap block count from GET LBA STATUS (CVE-2020-1711) (Felipe Franciosi)  [Orabug: 30807256]  {CVE-2020-1711}
- scsi: lsi: exit infinite loop while executing script (CVE-2019-12068) (Paolo Bonzini)  [Orabug: 30351703]  {CVE-2019-12068}
- lsi: use enum type for s->waiting (Sven Schnelle)   {CVE-2019-12068}
- json: Fix % handling when not interpolating (Christophe Fergeau)  [Orabug: 30640103] 
- qemu.spec: enable have_curl in spec (Dongli Zhang)  [Orabug: 30640103] 
- Fix heap overflow in ip_reass on big packet input (Samuel Thibault)  [Orabug: 30229916]  {CVE-2019-14378}
- Make poll_control_msr default 1 (Mark Kanda)  
- Remove redundant check for host support of halt polling (Mark Kanda)  [Orabug: 30240121] 
- Enable '-Werror' compiler flag (Mark Kanda)  [Orabug: 30213025] 
- qemu-submodule-init: Add Git submodule init script (Karl Heubaum)  [Orabug: 30729551]

* Thu Jun 27 2019 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-5.el7
- Only enable the halt poll control MSR if it is supported by the host (Mark
  Kanda)  [Orabug: 29946722]

* Wed Jun 19 2019 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-4.el7
- kvm: i386: halt poll control MSR support (Marcelo Tosatti)  [Orabug: 29933278] 
- Document CVEs as fixed: CVE-2017-9524, CVE-2017-6058, CVE-2017-5931 (Mark Kanda)  [Orabug: 29886908]  {CVE-2017-5931} {CVE-2017-6058} {CVE-2017-9524}
- pvrdma: release device resources in case of an error (Prasad J Pandit)  [Orabug: 29056678]  {CVE-2018-20123}
- qxl: check release info object (Prasad J Pandit)  [Orabug: 29886906]  {CVE-2019-12155}
- target/i386: add MDS-NO feature (Paolo Bonzini)  [Orabug: 29820428]  {CVE-2018-12126} {CVE-2018-12127} {CVE-2018-12130} {CVE-2019-11091}
- docs: recommend use of md-clear feature on all Intel CPUs (Daniel P. BerrangГ©)  [Orabug: 29820428]  {CVE-2018-12126} {CVE-2018-12127} {CVE-2018-12130} {CVE-2019-11091}
- target/i386: define md-clear bit (Paolo Bonzini)  [Orabug: 29820428]  {CVE-2018-12126} {CVE-2018-12127} {CVE-2018-12130} {CVE-2019-11091}
- pvh: block migration if booting using PVH (Liam Merwick)  [Orabug: 29796676] 
- hw/i386/pc: run the multiboot loader before the PVH loader (Stefano Garzarella)  [Orabug: 29796676] 
- optionrom/pvh: load initrd from fw_cfg (Stefano Garzarella)  [Orabug: 29796676] 
- hw/i386/pc: use PVH option rom (Stefano Garzarella)  [Orabug: 29796676] 
- qemu.spec: add pvh.bin to %files (Liam Merwick)  [Orabug: 29796676] 
- optionrom: add new PVH option rom (Stefano Garzarella)  [Orabug: 29796676] 
- linuxboot_dma: move common functions in a new header (Stefano Garzarella)  [Orabug: 29796676] 
- linuxboot_dma: remove duplicate definitions of FW_CFG (Stefano Garzarella)  [Orabug: 29796676] 
- pvh: load initrd and expose it through fw_cfg (Stefano Garzarella)  [Orabug: 29796676] 
- pvh: Boot uncompressed kernel using direct boot ABI (Liam Merwick)  [Orabug: 29796676] 
- pvh: Add x86/HVM direct boot ABI header file (Liam Merwick)  [Orabug: 29796676] 
- elf-ops.h: Add get_elf_note_type() (Liam Merwick)  [Orabug: 29796676] 
- elf: Add optional function ptr to load_elf() to parse ELF notes (Liam Merwick)  [Orabug: 29796676]

* Mon May 06 2019 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-3.el7
- x86: Document CVE-2018-12126 CVE-2018-12130 CVE-2018-12127 CVE-2019-11091 as
  fixed (Mark Kanda)  [Orabug: 29744956]  {CVE-2018-12126} {CVE-2018-12127}
  {CVE-2018-12130} {CVE-2019-11091}

* Wed May 01 2019 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-2.el7
- x86: Add mds feature (Karl Heubaum)  
- e1000: Never increment the RX undersize count register (Chris Kenna)  
- qemu.spec: audioflags set but never passed to configure script (Liam Merwick)  [Orabug: 29715562] 
- parfait: deal with parfait returning non-zero return value (Liam Merwick)  [Orabug: 29715548] 
- parfait: use nproc to choose default number of threads (Liam Merwick)  [Orabug: 29715548] 
- parfait: provide option to upload results (Liam Merwick)  [Orabug: 29715548] 
- parfait: disable misaligned-access check (Liam Merwick)  [Orabug: 29715548] 
- Document CVE-2019-8934 and CVE-2019-5008 as fixed (Mark Kanda)  [Orabug: 29715605]  {CVE-2019-5008} {CVE-2019-8934}
- device_tree.c: Don't use load_image() (Peter Maydell)  [Orabug: 29715527]  {CVE-2018-20815}
- slirp: check sscanf result when emulating ident (William Bowling)  [Orabug: 29715525]  {CVE-2019-9824}
- i2c-ddc: fix oob read (Gerd Hoffmann)  [Orabug: 29715520]  {CVE-2019-3812}
- scsi-generic: avoid possible out-of-bounds access to r->buf (Paolo Bonzini)  [Orabug: 29259700]  {CVE-2019-6501}
- slirp: check data length while emulating ident function (Prasad J Pandit)  [Orabug: 29715755]  {CVE-2019-6778}

* Wed Jan 16 2019 Mark Kanda <mark.kanda@oracle.com> - 15:3.1.0-1.el7
- vfio-pci: emit FAILOVER_PRIMARY_CHANGED event on guest behalf when unrealized
- vfio-pci: emit FAILOVER_PRIMARY_CHANGED event on guest behalf when unrealized (Si-Wei Liu)  [Orabug: 29216696] 
- vfio-pci: add FAILOVER_PRIMARY_CHANGED event to shorten downtime during failover (Si-Wei Liu)  [Orabug: 29216701] 
- virtio_net: Add support for "Data Path Switching" during Live Migration. (Venu Busireddy)  [Orabug: 29216704] 
- virtio_net: Introduce VIRTIO_NET_F_STANDBY feature bit to virtio_net (Sridhar Samudrala)  [Orabug: 29216714] 
- i386: Add some MSR based features on Cascadelake-Server CPU model (Tao Xu)  [Orabug: 29216681] 
- i386: Update stepping of Cascadelake-Server (Tao Xu)  [Orabug: 29216681] 
- usb-mtp: use O_NOFOLLOW and O_CLOEXEC. (Gerd Hoffmann)  [Orabug: 29216656]  {CVE-2018-16872}
- pvrdma: add uar_read routine (Prasad J Pandit)  [Orabug: 29216658]  {CVE-2018-20191}
- pvrdma: release ring object in case of an error (Prasad J Pandit)  [Orabug: 29216659]  {CVE-2018-20126}
- pvrdma: check number of pages when creating rings (Prasad J Pandit)  [Orabug: 29216666]  {CVE-2018-20125}
- pvrdma: check return value from pvrdma_idx_ring_has_ routines (Prasad J Pandit)  [Orabug: 29216672]  {CVE-2018-20216}
- rdma: remove unused VENDOR_ERR_NO_SGE macro (Prasad J Pandit)  [Orabug: 29216678]  {CVE-2018-20124}
- rdma: check num_sge does not exceed MAX_SGE (Prasad J Pandit)  [Orabug: 29216678]  {CVE-2018-20124}
- i386: Add "stibp" flag name (Eduardo Habkost)  
- parfait: Run static analysis when --with parfait specified (Liam Merwick)  [Orabug: 29216688] 
- parfait: add buildrpm/parfait-qemu.conf (Liam Merwick)  [Orabug: 29216688] 
- Document various CVEs as fixed (Mark Kanda)  [Orabug: 29212424]  {CVE-2017-10806} {CVE-2017-11334} {CVE-2017-12809} {CVE-2017-13672} {CVE-2017-13673} {CVE-2017-13711} {CVE-2017-14167} {CVE-2017-15038} {CVE-2017-15119} {CVE-2017-15124} {CVE-2017-15268} {CVE-2017-15289} {CVE-2017-16845} {CVE-2017-17381} {CVE-2017-18030} {CVE-2017-18043} {CVE-2017-2630} {CVE-2017-2633} {CVE-2017-5715} {CVE-2017-5753} {CVE-2017-5754} {CVE-2017-7471} {CVE-2017-7493} {CVE-2017-8112} {CVE-2017-8309} {CVE-2017-8379} {CVE-2017-8380} {CVE-2017-9503} {CVE-2018-10839} {CVE-2018-11806} {CVE-2018-12617} {CVE-2018-15746} {CVE-2018-16847} {CVE-2018-16867} {CVE-2018-17958} {CVE-2018-17962} {CVE-2018-17963} {CVE-2018-18849} {CVE-2018-19364} {CVE-2018-19489} {CVE-2018-3639} {CVE-2018-5683} {CVE-2018-7550} {CVE-2018-7858}
- qemu.spec: Initial qemu.spec (Mark Kanda)  
- virtio-pci: Set subsystem vendor ID to Oracle (Mark Kanda)  
- qemu_regdump.py: Initial qemu_regdump.py (Mark Kanda)  
- qmp-regdump: Initial qmp-regdump (Mark Kanda)  
- bridge.conf: Initial bridge.conf (Mark Kanda)  
- kvm.conf: Initial kvm.conf (Mark Kanda)  
- 80-kvm.rules: Initial 80-kvm.rules (Mark Kanda)


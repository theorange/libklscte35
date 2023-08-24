#!/bin/bash

set -e

rpm_base=libklscte35


_() {
	echo -e "\e[1;32m$@\e[0m"
	"$@"
}

_sudo() {
	if [ "$(id -u)" -ne 0 ]; then
		_ sudo "$@"
	else
		_ "$@"
	fi
}

install_deps() {
	rpm -q rpmdevtools || _sudo dnf install -y rpmdevtools yum-utils
	#_sudo dnf config-manager --set-enabled powertools
	_sudo dnf builddep -y ${rpm_base}.spec
}

build_rpm() {
	_ rpmdev-wipetree &> /dev/null || true
	_ rm -f ~/rpmbuild/SOURCES/master.zip
	_ find ~/rpmbuild/RPMS -name ${rpm_base}'-*.rpm' -delete || :
	_ rpmdev-setuptree &> /dev/null || true
	_ spectool -g -R ${rpm_base}.spec
	_ rpmbuild -ba ${rpm_base}.spec
	_ find ~/rpmbuild/RPMS -name ${rpm_base}'-*' -exec mv {} . \;
}

doit() {
	case "$1" in
	deps)
		install_deps
		;;
	rpm)
		build_rpm
		;;
	clean)
		_ rpmdev-wipetree
		_ rm -f ${rpm_base}*.rpm
		;;
	*)
		install_deps
		build_rpm
		;;
	esac
}

cmd="${1-all}"

while [ "$cmd" != "" ]; do
	doit "$cmd"
	shift
	cmd="$1"
done

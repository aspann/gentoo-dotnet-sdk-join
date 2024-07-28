# Copyright 1999-2024 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8
DISTUTILS_USE_PEP517=flit
PYTHON_COMPAT=( python3_{11..12} pypy3 )

inherit git-r3 python-r1 distutils-r1

DESCRIPTION="Tool to amalgamate dotnet SDKs for gentoo"
HOMEPAGE="https://github.com/aspann/gentoo-dotnet-sdk-join"
KEYWORDS="~*amd64 ~*arm ~*arm64"
LICENSE="MPL-2"
SLOT="9999"
IUSE="test"

EGIT_REPO_URI="https://github.com/aspann/gentoo-dotnet-sdk-join.git"
EGIT_BRANCH="dev/poc_test"

distutils_enable_tests pytest

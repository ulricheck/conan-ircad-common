#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from conans import ConanFile, tools
from fnmatch import fnmatch


def get_c_flags(**kwargs):
    if len(kwargs) > 0:
        is_posix = kwargs.get('is_posix', False)
        is_windows = kwargs.get('is_windows', False)
    else:
        is_posix = tools.os_info.is_posix
        is_windows = tools.os_info.is_windows

    if is_posix:
        return '-march=x86-64 -mtune=generic -mfpmath=sse -mmmx -msse -msse2 -msse3 -mssse3 -msse4.1 -msse4.2 -mavx -maes -mpclmul -mf16c'
    elif is_windows:
        return '/favor:blend /fp:strict /Qfast_transcendentals /arch:AVX /MP /bigobj /EHsc'
    else:
        return ''


def get_cxx_flags(**kwargs):
    return get_c_flags(**kwargs)


def get_cuda_version():
    return ['9.2', '10.0', 'None']


def get_cuda_arch():
    return ['3.0', '3.5', '5.0', '5.2', '6.1']


def fix_conan_dependency_path(conanfile, file_path, package_name):
    try:
        tools.replace_in_file(
            file_path,
            conanfile.deps_cpp_info[package_name].rootpath.replace('\\', '/'),
            "${CONAN_" + package_name.upper() + "_ROOT}",
            strict=False
        )
    except:
        conanfile.output.info("Ignoring {0}...".format(package_name))

def fix_conan_path(conanfile, root, wildcard):
    for path, subdirs, names in os.walk(root):
        for name in names:
            if fnmatch(name, wildcard):
                wildcard_file = os.path.join(path, name)

                tools.replace_in_file(
                    wildcard_file,
                    conanfile.package_folder.replace('\\', '/'),
                    '${CONAN_' + conanfile.name.upper() + '_ROOT}',
                    strict=False
                )

                for requirement in conanfile.requires:
                    fix_conan_dependency_path(conanfile, wildcard_file, requirement)


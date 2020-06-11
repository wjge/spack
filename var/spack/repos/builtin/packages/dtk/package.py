# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dtk(CMakePackage):
    """DataTransferKit is an open-source software library of parallel solution transfer services for multiphysics simulations"""

    homepage = "datatransferkit.readthedoc.io"
    url      = "https://github.com/ORNL-CEES/DataTransferKit/archive/3.1-rc1.tar.gz"
    git      = "https://github.com/ORNL-CEES/DataTransferKit.git"

    version('master', branch='master', submodules=True)

    variant('cuda', default=False, description='enable Cuda backend')
    variant('openmp', default=False, description='enable OpenMP backend')
    variant('serial', default=True, description='enable Serial backend (default)')

    depends_on('cmake', type='build')
    depends_on('trilinos@develop:~exodus+intrepid2~netcdf+shards', when='+serial')
    depends_on('cuda', when='+cuda')
    depends_on('trilinos@develop:~exodus+intrepid2~netcdf+shards+openmp', when='+openmp')

    def cmake_args(self):
        spec = self.spec

        options = [ 
            '-DBUILD_SHARED_LIBS=ON',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DDataTransferKit_ENABLE_DataTransferKit=ON',
            '-DDataTransferKit_ENABLE_TESTS=OFF',
            '-DDataTransferKit_ENABLE_EXAMPLES=OFF',
            '-DTPL_Trilinos_DIR=${TRILINOS_DIR}',
            '-DTPL_BoostOrg_INCLUDE_DIRS=${BOOST_DIR}/include',
            '-DCMAKE_CXX_EXTENSIONS=OFF',
            '-DCMAKE_CXX_STANDARD=14',
        ]

        if '+openmp' in spec:
            options.append('-DDataTransferKit_ENABLE_OpenMP=ON')

        if '+cuda' in spec:
            nvcc_wrapper_path = spec['kokkos'].prefix.bin.nvcc_wrapper
            options.append('-DCMAKE_CXX_COMPILER=%s' % nvcc_wrapper_path)

        return options

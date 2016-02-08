#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the pyqualtrics package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/Baguage/pyqualtrics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Use setuptools without bundling it
# https://pythonhosted.org/setuptools/setuptools.html#using-setuptools-without-bundling-it
# Note this means user will need network connection when running setup.py
# import ez_setup
# ez_setup.use_setuptools(version="18.2")

from setuptools import setup, find_packages

setup(
    name="pyqualtrics",
    version="0.4.0a",
    author="Alex Vyushkov",
    author_email="pyqualtrics@gmail.com",
    description="Unofficial python SDK for Qualtrics API",
    license="Apache License 2.0",
    keywords="API Qualtrics Survey SDK Social Science Psychology",
    url="https://github.com/Baguage/pyqualtrics",
    # find_packages() takes a source directory and two lists of package name patterns to exclude and include.
    # If omitted, the source directory defaults to the same directory as the setup script.
    packages=find_packages(exclude=["examples"]),  # https://pythonhosted.org/setuptools/setuptools.html#using-find-packages
    install_requires=["requests"],
    scripts=['bin/qualtrics.cmd', 'bin/qualtrics'],
    package_data = {
        # If any package contains *.qsf or *.rst files, include them:
        '': ['*.qsf', '*.rst'],
    },
    test_suite="pyqualtrics.tests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

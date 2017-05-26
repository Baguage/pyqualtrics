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

import sys
import os
from pyqualtrics import Qualtrics


try:
    # Python 2.7
    input = raw_input
except NameError:
    # Python 3.5
    pass


def main(argv):
    kwargs = {}
    iterator = iter(argv)
    executable = next(iterator)  # argv[0]
    try:
        command = next(iterator)     # argv[1]
    except StopIteration:
        print("The name of the API call to be made is required")
        return None

    user = None
    if "QUALTRICS_USER" not in os.environ:
        user = input("Enter Qualtrics username: ")

    token = None
    if "QUALTRICS_TOKEN" not in os.environ:
        token = input("Enter Qualtrics token: ")

    qualtrics = Qualtrics(user, token)
    method = getattr(qualtrics, command)
    if not method:
        print("%s API call is not implement" % method)
        return None

    for option in argv:
        try:
            arg, value = option.split("=")
            kwargs[arg] = value
        except ValueError:
            # Ignore parameter in wrong format
            pass
    return method(**kwargs)


if __name__ == "__main__":
    # main(["", "createPanel", "library_id=1", "name=b"])
    result = main(sys.argv)
    if result is None:
        print("Error executing API Call")
    else:
        print("Success: %s" % result)

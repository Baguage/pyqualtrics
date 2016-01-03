# Copyright (C) 2015, University of Notre Dame
# All rights reserved

import sys
import os
from pyqualtrics import Qualtrics


def main(argv):
    kwargs = {}
    iterator = iter(argv)
    executable = iterator.next()  # argv[0]
    try:
        command = iterator.next()     # argv[1]
    except StopIteration:
        print "The name of the API call to be made is required"
        return None

    user = None
    if "QUALTRICS_USER" not in os.environ:
        user = raw_input("Enter Qualtrics username: ")

    token = None
    if "QUALTRICS_TOKEN" not in os.environ:
        token = raw_input("Enter Qualtrics token: ")

    qualtrics = Qualtrics(user, token)
    method = getattr(qualtrics, command)
    if not method:
        print "%s API call is not implement" % method
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
        print "Error executing API Call"
    else:
        print "Success: %s" % result

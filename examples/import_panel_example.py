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

from pyqualtrics import Qualtrics
import os

user = None   # os.environ["QUALTRICS_USER"]
token = None  # os.environ["QUALTRICS_TOKEN"]

if __name__ == "__main__":
    print "This is an example of panel import"
    print "Make sure you have set QUALTRICS_USER, QUALTRICS_TOKEN and QUALTRICS_LIBRARY_ID enviroment variable"

    # Note is user and token are None, QUALTRICS_USER and QUALTRICS_TOKEN environment variables will be used instead
    qualtrics = Qualtrics(user, token)
    library_id = os.environ["QUALTRICS_LIBRARY_ID"]
    panel_id = qualtrics.importJsonPanel(
        library_id,
        Name="New Panel Created by PyQualtrics library (DELETE ME)",
        panel=[
            {"Email": "pyqualtrics+1@gmail.com", "FirstName": "PyQualtrics", "LastName": "Library", "SubjectID": "123"},
            {"Email": "pyqualtrics+2@gmail.com", "FirstName": "PyQualtrics2", "LastName": "Library2"}
        ],
        headers=["Email", "FirstName", "LastName", "ExternalRef", "SubjectID"],
        AllED=1)
    if qualtrics.last_error_message:
        print "Error creating panel: " + qualtrics.last_error_message
    else:
        print "Panel created successfully, PanelID: " + panel_id

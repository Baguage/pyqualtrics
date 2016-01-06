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
import random
import string
from pyqualtrics import Qualtrics
import os

user = None   # os.environ["QUALTRICS_USER"]
token = None  # os.environ["QUALTRICS_TOKEN"]

if __name__ == "__main__":
    print "This is an example of sending a survey"
    print "Make sure you have set QUALTRICS_USER, QUALTRICS_TOKEN, QUALTRICS_LIBRARY_ID, QUALTRICS_SURVEY_ID " \
          "and QUALTRICS_MESSAGE_ID enviroment variables"

    # Note is user and token are None, QUALTRICS_USER and QUALTRICS_TOKEN environment variables will be used instead
    qualtrics = Qualtrics(user, token)

    library_id = os.environ["QUALTRICS_LIBRARY_ID"]
    survey_id = os.environ["QUALTRICS_SURVEY_ID"]
    message_id = os.environ["QUALTRICS_MESSAGE_ID"]

    panel_id = qualtrics.createPanel(
        library_id=library_id,
        name="Test Panel created by pyqualtrics example (DELETE ME)"
    )

    if panel_id is None:
        print "Error creating panel: %s" % qualtrics.last_error_message
        sys.exit(-1)

    # random_prefix is required because you can't send same survey to the same email twice
    random_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    recipient_id = qualtrics.addRecipient(
        library_id,
        panel_id,
        FirstName="Subject",
        LastName="Name",
        Email="PyQualtrics+%s@gmail.com" % random_prefix,
        ExternalDataRef="SUBJ0001",
        Language="EN",
        ED={"SubjectID": "SUBJ0001"}  # Embedded Data as python dictionary.
    )

    if recipient_id is None:
        print "Error adding recipient: %s" % qualtrics.last_error_message
        sys.exit(-1)

    distribution_id = qualtrics.sendSurveyToIndividual(
        SendDate="2015-12-12 19:48:28",
        FromEmail="noreply@qemailserver.com",
        FromName="PyQualtrics Library",
        MessageID=message_id,
        MessageLibraryID=library_id,
        Subject="Why, hello there",
        SurveyID=survey_id,
        PanelID=panel_id,
        PanelLibraryID=library_id,
        RecipientID=recipient_id
    )

    if distribution_id is None:
        print "Error sending email: %s" % qualtrics.last_error_message

    result = qualtrics.deletePanel(
         library_id=library_id,
         panel_id=panel_id
    )

    if not result:
        print "Can't delete panel: %s" % qualtrics.last_error_message

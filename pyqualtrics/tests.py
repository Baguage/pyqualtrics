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

""" Unittests for the pyqualtrics package
"""

import random
import string

from pyqualtrics import Qualtrics
import unittest
import os


class TestQualtrics(unittest.TestCase):
    def setUp(self):
        self.user = os.environ["QUALTRICS_USER"]
        self.token = os.environ["QUALTRICS_TOKEN"]
        self.library_id = os.environ["QUALTRICS_LIBRARY_ID"]
        self.survey_id = os.environ.get("QUALTRICS_SURVEY_ID", None)
        self.message_id = os.environ.get("QUALTRICS_MESSAGE_ID", None)
        self.response_id = os.environ.get("QUALTRICS_RESPONSE_ID", None)
        self.qualtrics = Qualtrics(self.user, self.token)

    def test_str(self):
        self.assertEqual(str(self.qualtrics), self.user)

    def test_creation_errors(self):
        panel_id = self.qualtrics.createPanel(LibraryID="",
                                              Name="Hello",
                                              User="deadbeaf")
        self.assertIsNone(panel_id)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        # message can be "Incorrect Username or Password" or "User Account Disabled"
        # self.assertEqual(self.qualtrics.last_error_message, "Incorrect Username or Password")

        # We can't really test for invalid token error, because Qualtrics disables account
        # if there are too many failed login attempts.
        # For example:
        #     "Too many failed login attempts. Your account has been disabled for 10 minutes."
        # self.assertEqual(message, "Invalid token")

        # Create panel with non-existing library id
        panel_id = self.qualtrics.createPanel(
                                      LibraryID="",
                                      Name="Hello")
        self.assertIsNone(panel_id)
        self.assertEqual(self.qualtrics.last_error_message,
                         "Invalid request. Missing or invalid parameter LibraryID.")

    def test_create_and_delete(self):
        # Note you may need to login and logout to see new panel in Qualtrics interface
        panel_id = self.qualtrics.createPanel(
            LibraryID=self.library_id,
            Name="Test Panel created by pyqualtrics library (DELETE ME)"
        )
        self.assertIsNotNone(panel_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)

        # random_prefix is required because you can't send same survey to the same email twice
        random_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        recipient_id = self.qualtrics.addRecipient(
            self.library_id,
            panel_id,
            FirstName="Fake",
            LastName="Subject",
            Email="PyQualtrics+%s@gmail.com" % random_prefix,
            ExternalDataRef=None,
            Language="EN",
            ED={"SubjectID": "123"}
        )
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(recipient_id)

        recipient = self.qualtrics.getRecipient(LibraryID=self.library_id, RecipientID=recipient_id)
        self.assertEqual(recipient["FirstName"], "Fake")
        self.assertEqual(recipient["LastName"], "Subject")
        self.assertEqual(recipient["Language"], "EN")
        self.assertIsNone(recipient["ExternalDataReference"])
        self.assertEqual(recipient["EmbeddedData"]["SubjectID"], "123")

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 1)

        if self.survey_id is not None and self.message_id is not None:
            # Test email delivery if SurveyID and MessageID have been provided
            distribution_id = self.qualtrics.sendSurveyToIndividual(SendDate="2015-12-12 19:48:28",
                                                  FromEmail="noreply@qemailserver.com",
                                                  FromName="PyQualtrics Library",
                                                  MessageID=self.message_id,
                                                  MessageLibraryID=self.library_id,
                                                  Subject="Why, hello there",
                                                  SurveyID=self.survey_id,
                                                  PanelID=panel_id,
                                                  PanelLibraryID=self.library_id,
                                                  RecipientID=recipient_id)
            self.assertIsNotNone(distribution_id)
            self.assertIsNone(self.qualtrics.last_error_message)
            self.assertIsNotNone(self.qualtrics.json_response)

            result = self.qualtrics.getDistributions(LibraryID=self.library_id,
                                                     SurveyID=self.survey_id,
                                                     DistributionID=distribution_id)
            self.assertIsNotNone(result)

            xml = self.qualtrics.getSurvey(SurveyID=self.survey_id)
            self.assertIsNotNone(xml)
            self.assertIsNone(self.qualtrics.json_response)
            self.assertIsNone(self.qualtrics.last_error_message)

            data = self.qualtrics.getLegacyResponseData(SurveyID=self.survey_id)
            self.assertIsNotNone(data)
            self.assertIsNotNone(self.qualtrics.json_response)
            self.assertIsNone(self.qualtrics.last_error_message)

        if self.response_id is not None and self.survey_id is not None:
            response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID=self.response_id)
            self.assertIsNotNone(response)
            self.assertIsNone(self.qualtrics.last_error_message)

            response = self.qualtrics.getResponse(SurveyID=self.survey_id, ResponseID="abc")
            self.assertIsNone(response)
            self.assertEqual(self.qualtrics.last_error_message, "Invalid request. Missing or invalid parameter ResponseID.")  # noqa

        result = self.qualtrics.removeRecipient(LibraryID=self.library_id,
                                                PanelID=panel_id,
                                                RecipientID=recipient_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertEqual(result, True)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)

        result = self.qualtrics.deletePanel(
                             LibraryID=self.library_id,
                             PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

    def test_panel_errors(self):
        result = self.qualtrics.removeRecipient(LibraryID=self.library_id,
                                                PanelID="",
                                                RecipientID="")
        self.assertEqual(result, False)
        self.assertEqual(
            self.qualtrics.last_error_message,
            "Invalid request. Missing or invalid parameter RecipientID."
        )

    def test_deletion_errors(self):
        result = self.qualtrics.deletePanel(LibraryID="",
                                            PanelID="",
                                            User="deadbeaf")
        self.assertEqual(result, False)
        self.assertIsNotNone(self.qualtrics.last_error_message)
        # Different error messages can be returned
        # "Incorrect Username or Password"
        # "Account Locked"

        # We can't really test for invalid token error, because Qualtrics disables account
        # if there are too many failed login attempts
        # For example:
        #     "Too many failed login attempts. Your account has been disabled for 10 minutes."

        result = self.qualtrics.deletePanel(LibraryID="",
                                            PanelID="Hello")
        self.assertEqual(result, False)
        self.assertEqual(self.qualtrics.last_error_message,
                         "Invalid request. Missing or invalid parameter LibraryID.")

    def test_json_import(self):
        panel_id = self.qualtrics.importJsonPanel(
            self.library_id,
            Name="Panel for testing JSON Import",
            panel=[
                    {"Email": "pyqualtrics+1@gmail.com", "FirstName": "PyQualtrics", "LastName": "Library"},
                    {"Email": "pyqualtrics+2@gmail.com", "FirstName": "PyQualtrics2", "LastName": "Library2"}
                  ])
        self.assertIsNotNone(panel_id)
        self.assertIsNotNone(self.qualtrics.json_response)
        self.assertIsNone(self.qualtrics.last_error_message)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 2)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        subjects = self.qualtrics.getPanel(self.library_id, panel_id)
        self.assertEqual(len(subjects), 2)
        self.assertEqual(subjects[0]["LastName"], "Library")
        self.assertEqual(subjects[1]["FirstName"], "PyQualtrics2")


        new_panel_id = self.qualtrics.importJsonPanel(
            self.library_id,
            Name="Panel for testing JSON Import",
            PanelID=panel_id,
            panel=[
                    {"Email": "pyqualtrics+3@gmail.com", "FirstName": "PyQualtrics", "LastName": "Library3"},
                    {"Email": "pyqualtrics+4@gmail.com", "FirstName": "PyQualtrics2", "LastName": "Library4"}
                  ])

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 4)
        self.assertEqual(new_panel_id, panel_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        # This one should not be successful
        result = self.qualtrics.importJsonPanel(
            self.library_id,
            Name="Panel for testing JSON Import",
            PanelID=panel_id,
            headers=["FirstName", "LastName"],
            panel=[
                    {"FirstName": "PyQualtrics", "LastName": "Library3"},
                    {"FirstName": "PyQualtrics2", "LastName": "Library4"}
                  ])
        self.assertEqual(result, None)
        self.assertEqual(self.qualtrics.last_error_message, "Invalid request. Missing or invalid parameter Email.")

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 4)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        result = self.qualtrics.deletePanel(
                             LibraryID=self.library_id,
                             PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

    def test_json_import_with_embedded_data(self):
        panel_id = self.qualtrics.importJsonPanel(
            self.library_id,
            Name="Panel for testing JSON Import",
            panel=[
                    {"Email": "pyqualtrics+1@gmail.com", "FirstName": "PyQualtrics", "LastName": "Library", "SubjectID": "SUBJ0001"},  # noqa
                    {"Email": "pyqualtrics+2@gmail.com", "FirstName": "PyQualtrics2", "LastName": "Library2"}
                  ],
            headers=["Email", "FirstName", "LastName", "ExternalRef", "SubjectID"],
            AllED=1)
        self.assertIsNotNone(panel_id)
        self.assertIsNotNone(self.qualtrics.json_response)
        self.assertIsNone(self.qualtrics.last_error_message)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 2)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        subjects = self.qualtrics.getPanel(self.library_id, panel_id)
        self.assertEqual(len(subjects), 2)
        self.assertEqual(subjects[0]["LastName"], "Library")
        self.assertEqual(subjects[1]["FirstName"], "PyQualtrics2")
        self.assertEqual(subjects[0]["EmbeddedData"]["SubjectID"], "SUBJ0001")

        result = self.qualtrics.deletePanel(
                             LibraryID=self.library_id,
                             PanelID=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

if __name__ == "__main__":
    unittest.main()

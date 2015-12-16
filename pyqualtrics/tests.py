# Copyright (C) 2015, University of Notre Dame
# All rights reserved
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
        self.qualtrics = Qualtrics(self.user, self.token)

    def test_creation_errors(self):
        panel_id = self.qualtrics.createPanel(library_id="",
                                              name="Hello",
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
                                      library_id="",
                                      name="Hello")
        self.assertIsNone(panel_id)
        self.assertEqual(self.qualtrics.last_error_message,
                         "Invalid request. Missing or invalid parameter LibraryID.")

    def test_create_and_delete(self):
        # Note you may need to login and logout to see new panel in Qualtrics interface
        panel_id = self.qualtrics.createPanel(library_id=self.library_id,
                                                      name="Test Panel created by pyqualtrics library (DELETE ME)")
        self.assertIsNotNone(panel_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)

        random_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        recipient_id = self.qualtrics.addRecipient(self.library_id, panel_id,
                                    FirstName="Fake", LastName="Subject", Email="PyQualtrics+%s@gmail.com" % random_prefix,
                                    ExternalDataRef=None, Language="EN", ED={"SubjectID": "123"})
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

        result = self.qualtrics.removeRecipient(LibraryID=self.library_id,
                                                PanelID=panel_id,
                                                RecipientID=recipient_id)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertEqual(result, True)

        count = self.qualtrics.getPanelMemberCount(self.library_id, panel_id)
        self.assertEqual(count, 0)

        result = self.qualtrics.deletePanel(
                             library_id=self.library_id,
                             panel_id=panel_id)
        self.assertEqual(result, True)
        self.assertIsNone(self.qualtrics.last_error_message)
        self.assertIsNotNone(self.qualtrics.json_response)

    def test_panel_errors(self):
        result = self.qualtrics.removeRecipient(LibraryID=self.library_id,
                                                PanelID="",
                                                RecipientID="")
        self.assertEqual(result, False)
        self.assertEqual(self.qualtrics.last_error_message, "Invalid request. Missing or invalid parameter RecipientID.")

    def test_deletion_errors(self):
        result = self.qualtrics.deletePanel(library_id="",
                                            panel_id="",
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

        result = self.qualtrics.deletePanel(library_id="",
                                            panel_id="Hello")
        self.assertEqual(result, False)
        self.assertEqual(self.qualtrics.last_error_message,
                         "Invalid request. Missing or invalid parameter LibraryID.")

if __name__ == "__main__":
    unittest.main()
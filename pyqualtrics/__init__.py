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

import csv
import json
from StringIO import StringIO
import requests
import os

class Qualtrics(object):
    """
    This is representation of Qualtrics REST API
    """
    url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php"

    def __init__(self, user=None, token=None, api_version="2.5"):
        """
        :param user: The user name. If omitted, value of environment variable QUALTRICS_USER will be used.
        :param token: API token for the user. If omitted, value of environment variable QUALTRICS_TOKEN will be used.
        :param api_version: API version to use (this library has been tested with version 2.5).
        """
        if user is None:
            user = os.environ.get("QUALTRICS_USER", None)
        if user is None:
            raise ValueError("user parameter should be passed to __init__ or enviroment variable  QUALTRICS_USER should be set")  # noqa
        self.user = user

        if token is None:
            token = os.environ.get("QUALTRICS_TOKEN", None)
        if token is None:
            raise ValueError("token parameter should be passed to __init__ or enviroment variable QUALTRICS_TOKEN should be set")  # noqa
        self.token = token
        self.default_api_version = api_version
        # Version must be a string, not an integer or float
        assert self.default_api_version, (str, unicode)
        self.last_error_message = None
        self.last_url = None
        self.json_response = None

    def __str__(self):
        return self.user

    def __repr__(self):
        # Used code snippet from stackoverflow
        # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
        # Note this will print Qualtrics token - may be dangerous for logging
        return "%s(%r)" % (self.__class__, self.__dict__)

    def request(self, Request, post_data=None, **kwargs):
        """ Send GET or POST request to Qualtrics API
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#overview_2.5

        This function also sets self.last_error_message and self.json_response

        :param Request: The name of the API call to be made ("createPanel", "deletePanel" etc).
        :param post_data: Content of POST request. If None, GET request will be sent
        :param kwargs: Additional parameters for this API Call (LibraryID="abd", PanelID="123")
        :return: None if request failed
        """
        Version = kwargs.pop("Version", self.default_api_version)
        # Version must be a string, not an integer or float
        assert Version, (str, unicode)

        # Special case for handling embedded data
        ed = kwargs.pop("ED", None)

        # http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
        params = dict({"User": self.user,
                       "Token": self.token,
                       "Format": "JSON",
                       "Version": Version,
                       "Request": Request,
                       }.items() + kwargs.items())

        # Format emdedded data properly,
        # for example ED[SubjectID]=1CLE10235&ED[Zip]=74534
        if ed is not None:
            for key in ed:
                params["ED[%s]" % key] = ed[key]

        if post_data:
            r = requests.post(self.url,
                              data=post_data,
                              params=params)
        else:
            r = requests.get(self.url,
                             params=params)
        self.last_url = r.url
        try:
            json_response = json.loads(r.text)
        except ValueError:
            # If the data being deserialized is not a valid JSON document, a ValueError will be raised.
            self.json_response = None
            if "Format" not in kwargs:
                self.last_error_message = "Unexpected response from Qualtrics: not a JSON document"
                raise RuntimeError(self.last_error_message)
            else:
                # Special case - getSurvey. That request has a custom response format (xml).
                # It does not follow the default response format
                return r.text

        self.json_response = json_response
        # Sanity check.
        if (Request == "getLegacyResponseData" or Request == "getPanel") and "Meta" not in json_response:
            # Special cases - getLegacyResponseData and getPanel
            # Success
            return json_response
        if "Meta" not in json_response:
            # Should never happen
           self.last_error_message = "Unexpected response from Qualtrics: no Meta key in JSON response"
           raise RuntimeError(self.last_error_message)
        if "Status" not in json_response["Meta"]:
            # Should never happen
            self.last_error_message = "Unexpected response from Qualtrics: no Status key in JSON response"
            raise RuntimeError(self.last_error_message)

        if json_response["Meta"]["Status"] == "Success":
            self.last_error_message = None
            return json_response

        # If error happens, it returns JSON object too
        # Error message is in json_response["Meta"]["ErrorMessage"]
        self.last_error_message = json_response["Meta"]["ErrorMessage"]
        return None

    def createPanel(self, LibraryID, Name, **kwargs):
        """ Creates a new Panel in the Qualtrics System and returns the id of the new panel
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#createPanel_2.5

        :param LibraryID: 	The library id you want to create the panel in
        :param Name: The name of the new panel
        :return: PanelID of new panel, None if error occurs
        """
        if self.request("createPanel", LibraryID=LibraryID, Name=Name, **kwargs) is None:
            return None
        return self.json_response["Result"]["PanelID"]

    def deletePanel(self, LibraryID, PanelID, **kwargs):
        """ Deletes the panel.
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#deletePanel_2.5

        :param LibraryID: The library id the panel is in.
        :param PanelID: The panel id that will be deleted.
        :return: True if deletion was successful, False otherwise
        """
        if self.request("deletePanel", LibraryID=LibraryID, PanelID=PanelID, **kwargs) is None:
            return False
        return True

    def getPanelMemberCount(self, LibraryID, PanelID, **kwargs):
        """ Gets the number of panel members
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getPanelMemberCount_2.5
        :param LibraryID: The library ID where this panel belongs
        :param PanelID: The panel ID
        :param kwargs: Additional parameters (used by unittest)
        :return: The Number of members
        """
        if self.request("getPanelMemberCount", LibraryID=LibraryID, PanelID=PanelID, **kwargs) is None:
            return None
        return int(self.json_response["Result"]["Count"])

    def addRecipient(self, LibraryID, PanelID, FirstName, LastName, Email, ExternalDataRef, Language, ED):
        """ Add a new recipient to a panel
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#addRecipient_2.5

        :param LibraryID: The library the recipient belongs to
        :param PanelID: 	The panel to add the recipient
        :param FirstName:  	The first name
        :param LastName: 	The last name
        :param Email:  	The email address
        :param ExternalDataRef: 	The external data reference
        :param Language: 	The language code
        :param ED:  	The embedded data (dictionary)
        :return: 	The Recipient ID or None
        """
        if not self.request("addRecipient",
                            LibraryID=LibraryID,
                            PanelID=PanelID,
                            FirstName=FirstName,
                            LastName=LastName,
                            Email=Email,
                            ExternalDataRef=ExternalDataRef,
                            Language=Language,
                            ED=ED):
            return None
        return self.json_response["Result"]["RecipientID"]

    def getRecipient(self, LibraryID, RecipientID):
        """Get a representation of the recipient and their history
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getRecipient_2.5

        :param LibraryID: The library the recipient belongs to
        :param RecipientID: The recipient id of the person's response history you want to retrieve
        """
        if not self.request("getRecipient", LibraryID=LibraryID, RecipientID=RecipientID):
            return None
        return self.json_response["Result"]["Recipient"]

    def removeRecipient(self, LibraryID, PanelID, RecipientID, **kwargs):
        """ Removes the specified panel member recipient from the specified panel.
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#removeRecipient_2.5

        :param LibraryID: The library the recipient belongs to
        :param PanelID: The panel to remove the recipient from
        :param RecipientID: The recipient id of the person that will be updated
        :return: True if successful, False otherwise
        """
        if not self.request("removeRecipient", LibraryID=LibraryID, PanelID=PanelID, RecipientID=RecipientID, **kwargs):
            return False
        return True

    def sendSurveyToIndividual(self, **kwargs):
        """ Sends a survey through the Qualtrics mailer to the individual specified.
        Note that request will be put to queue and emails are not sent immediately (although they usually
        delivered in a few seconds after this function is complete)

        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#sendSurveyToIndividual_2.5
        :param kwargs:
        :return: DistributionID
        """
        if not self.request("sendSurveyToIndividual", **kwargs):
            return None
        return self.json_response["Result"]["EmailDistributionID"]

    def getDistributions(self, **kwargs):
        """ Returns the data for the given distribution.
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getDistributions_2.5

        Requests for distribution surveys to users are queued and not delivered immediately. Thus
        functions like sendSurveyToIndividual will successfully completed even though no email were sent yet.
        DistributionID returned by those functions can be used to check status of email delivery.

        :param kwargs:
        :return:
        """
        if not self.request("getDistributions", **kwargs):
            return None
        return self.json_response

    def getSurvey(self, SurveyID):
        # Good luck dealing with XML
        # Response does not include answers though
        return self.request("getSurvey", SurveyID=SurveyID, Format=None)

    def getLegacyResponseData(self, SurveyID, **kwargs):
        """ Returns all of the response data for a survey in the original (legacy) data format.
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getLegacyResponseData_2.5

        :param SurveyID: 	The survey you will be getting the responses for.
        :param kwargs: Additional parameters allowed by getLegacyResponseData API call
        :return:
        """
        return self.request("getLegacyResponseData", SurveyID=SurveyID, **kwargs)

    def getResponse(self, SurveyID, ResponseID, **kwargs):
        """ Get data for a single response ResponseID in SurveyID. SurveyID is required by API
        Refer to https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getLegacyResponseData_2.5 for additional
        information about kwargs

        :param SurveyID: The survey you will be getting the responses for.
        :param ResponseID: The response id of an individual response.
        :param kwargs: Additional arguments (Labels, Questions, ExportQuestionID, ExportTags, LocalTime, etc)
        :return: response as Python dictionary.
        Example:
        {u'Status': u'0', u'StartDate': u'2015-10-23 10:59:12', u'Q1': 2, u'Q2': 1, u'EndDate': u'2015-10-23 10:59:23',
        u'Name': u'Freeborni, Anopheles', u'IPAddress': u'129.74.236.110', u'Q3': 2, u'ExternalDataReference': u'',
        u'Finished': u'1', u'EmailAddress': u'pyqualtrics+2@gmail.com', u'ResponseSet': u'Default Response Set'}
        """
        response = self.getLegacyResponseData(SurveyID=SurveyID, ResponseID=ResponseID, **kwargs)
        if not response:
            return None
        if ResponseID not in response:
            # Should never happen
            self.last_error_message = "Qualtrics error: ResponseID %s not in response" % ResponseID
            return None
        return response[ResponseID]

    def getPanel(self, LibraryID, PanelID, EmbeddedData=None, LastRecipientID=None, NumberOfRecords=None,
                 ExportLanguage=None, Unsubscribed=None, Subscribed=None, **kwargs):
        """ Gets all the panel members for the given panel
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getPanel_2.5
        :param LibraryID: The library id for this panel
        :param PanelID:  	The panel id you want to export
        :param EmbeddedData: A comma separated list of the embedded data keys you want to export. This is only required for a CSV export.
        :param LastRecipientID: The last Recipient ID from a previous API call. Start returning everyone AFTER this Recipient
        :param NumberOfRecords: 	The number of panel members to return. If not defined will return all of them
        :param ExportLanguage: 	If 1 the language of each panel member will be exported.
        :param Unsubscribed: If 1 only the unsubscribed panel members will be returned
        :param Subscribed:	If 1 then only subscribed panel members will be returned
        :return: list of panel member as dictionaries
        """
        if not self.request("getPanel",
                            LibraryID=LibraryID,
                            PanelID=PanelID,
                            EmbeddedData=EmbeddedData,
                            LastRecipientID=LastRecipientID,
                            NumberOfRecords=NumberOfRecords,
                            ExportLanguage=ExportLanguage,
                            Unsubscribed=Unsubscribed,
                            Subscribed=Subscribed,
                            **kwargs):
            return None
        return self.json_response

    def importPanel(self, LibraryID, Name, CSV, **kwargs):
        """ Imports a csv file as a new panel (optionally it can append to a previously made panel) into the database
        and returns the panel id.  The csv file can be posted (there is an approximate 8 megabytes limit)  or a url can
        be given to retrieve the file from a remote server.
        The csv file must be comma separated using " for encapsulation.

        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#importPanel_2.5

        :param LibraryID:
        :param Name:
        :param CSV: contents of CSV file to be imported
        :return:
        """

        if kwargs.get("ColumnHeaders", None) == "1" or kwargs.get("ColumnHeaders", None) == 1:
            fp = StringIO(CSV)
            headers = csv.reader(fp).next()
            if "Email" in headers and "Email" not in kwargs:
                kwargs["Email"] = headers.index("Email") + 1
            if "FirstName" in headers and "FirstName" not in kwargs:
                kwargs["FirstName"] = headers.index("FirstName") + 1
            if "LastName" in headers and "LastName" not in kwargs:
                kwargs["LastName"] = headers.index("LastName") + 1
            if "ExternalRef" in headers and "ExternalRef" not in kwargs:
                kwargs["ExternalRef"] = headers.index("ExternalRef") + 1
            fp.close()

        result = self.request("importPanel", post_data=CSV, LibraryID=LibraryID, Name=Name, **kwargs)
        if result is not None:
            return result["Result"]["PanelID"]
        return None

    def importJsonPanel(self, LibraryID, Name, panel, headers=None, **kwargs):
        """ Import JSON document as a new panel. Example document:
        [
        {"Email": "pyqualtrics@gmail.com", "FirstName": "PyQualtrics", "LastName": "Library"},
        {"Email": "pyqualtrics+2@gmail.com", "FirstName": "PyQualtrics2", "LastName": "Library2"}
        ]

        :param LibraryID:
        :param Name:
        :param panel:
        :param kwargs:
        :return:
        """
        if headers is None:
            headers = ["Email", "FirstName", "LastName", "ExternalRef"]
        buffer = str()
        fp = StringIO(buffer)
        dictwriter = csv.DictWriter(fp, fieldnames=headers)
        dictwriter.writeheader()
        for subject in panel:
            dictwriter.writerow(subject)

        CSV = fp.getvalue()
        return self.importPanel(LibraryID=LibraryID,
                                Name=Name,
                                CSV=CSV,
                                ColumnHeaders="1",
                                **kwargs
                                )

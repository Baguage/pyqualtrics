import json
import requests


class Qualtrics(object):
    """
    This is representation of Qualtrics REST API
    """
    url = "https://survey.qualtrics.com/WRAPI/ControlPanel/api.php"

    def __init__(self, user, token, api_version="2.5"):
        """
        :param user: The user name.
        :param token: API token for the user.
        :param library_id: The library id the panel is in.
        """
        self.user = user
        self.token = token
        self.default_api_version = api_version
        # Version must be a string, not an integer or float
        assert self.default_api_version, (str, unicode)
        self.last_error_message = None
        self.last_url = None
        self.json_response = None

    def request(self, Request, **kwargs):
        """ Send GET request to Qualtrics API
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#overview_2.5

        This function also sets self.last_error_message and self.json_response

        :param Request: The name of the API call to be made (createPanel, deletePanel etc).
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
        if Request == "getLegacyResponseData" and "Meta" not in json_response:
            # Special case - getLegacyResponseData
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

    def createPanel(self, library_id, name, **kwargs):
        """ Creates a new Panel in the Qualtrics System and returns the id of the new panel
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#createPanel_2.5

        :param library_id: 	The library id you want to create the panel in
        :param name: The name of the new panel
        :return: PanelID of new panel, None if error occurs
        """
        if self.request("createPanel", LibraryID=library_id, Name=name, **kwargs) is None:
            return None
        return self.json_response["Result"]["PanelID"]

    def deletePanel(self, library_id, panel_id, **kwargs):
        """ Deletes the panel.
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#deletePanel_2.5

        :param library_id: The library id the panel is in.
        :param panel_id: The panel id that will be deleted.
        :return: True if deletion was successful, False otherwise
        """
        if self.request("deletePanel", LibraryID=library_id, PanelID=panel_id, **kwargs) is None:
            return False
        return True

    def getPanelMemberCount(self, library_id, panel_id, **kwargs):
        """ Gets the number of panel members
        https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#getPanelMemberCount_2.5
        :param library_id: The library ID where this panel belongs
        :param panel_id: The panel ID
        :param kwargs: Additional parameters (used by unittest)
        :return: The Number of members
        """
        if self.request("getPanelMemberCount", LibraryID=library_id, PanelID=panel_id, **kwargs) is None:
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

    def sendSurveyToIndividual(self, **kwargs):
        """ Sends a survey through the Qualtrics mailer to the individual specified.
        Note that request will be put to queue and emails are not sent immediately (altough they usually
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

from pyqualtrics import Qualtrics
import os

user = None
token = None

if __name__ == "__main__":
    print "This is an example of sending a survey"
    print "Make sure you have set QUALTRICS_USER, QUALTRICS_TOKEN, QUALTRICS_LIBRARY_ID, QUALTRICS_SURVEY_ID " \
          "and QUALTRICS_MESSAGE_ID enviroment variables"

    # Note is user and token are None, QUALTRICS_USER and QUALTRICS_TOKEN environment variables will be used instead
    qualtrics = Qualtrics(user, token)

    survey_id = os.environ["QUALTRICS_SURVEY_ID"]

    qualtrics = Qualtrics(user, token)
    responses = qualtrics.getLegacyResponseData(SurveyID=survey_id)
    for response_id, response in responses.items():
        print response_id + " - " + response["Finished"]


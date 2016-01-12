[![Downloads](https://img.shields.io/pypi/dw/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)
[![Version](https://img.shields.io/pypi/v/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)
[![License](https://img.shields.io/pypi/l/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)
[![Python](https://img.shields.io/pypi/pyversions/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)

PyQualtrics
=====

Unofficial python SDK for Qualtrics API

# System requirements

Python 2.7 only. Requires setuptools. 
Run `python ez_setup.py` command if you do not have setuptools installed in your virtual environment.

# Installation

Install using pip:

`pip install pyqualtrics`

Development version can installed using `pip install git+https://github.com/Baguage/pyqualtrics.git`

Alternatively, you can download or clone this repo and call `pip install -e ..`

# Usage example

This library requires account with Qualtrics API enabled. Check with your Qualtrics representative to see if API 
Access is available for your account. 

Please refer to http://www.qualtrics.com/university/researchsuite/developer-tools/api-integration/qualtrics-rest-api/ 
for information on how to get your API Token and other Qualtrics IDs.

```python
from pyqualtrics import Qualtrics

qualtrics = Qualtrics(QUALTRICS_USER, QUALTRICS_TOKEN)
responses = qualtrics.getLegacyResponseData(SurveyID=QUALTRICS_SURVEY_ID)
for response_id, response in response.itemitem():
    print response_id + " - " + response["Finished"]
```

# Documentation

Full documenation is not yet available.

# How to run tests

Tests suite requires access to Qualtrics API. It uses following environment variables

QUALTRICS_USER	- Qualtrics User ID

QUALTRICS_TOKEN	- Token to access Qualtrics API

QUALTRICS_LIBRARY_ID - Library ID

If either of these variables is not define, tests won't start at all.

If you want to run full test suite, you may want to create a survey, a message and one response in your Qualtrics account.
QUALTRICS_SURVEY_ID, QUALTRICS_RESPONSE_ID and QUALTRICS_MESSAGE_ID variable should be set to activate those tests


# Bugs and requests

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/Baguage/pyqualtrics/issues

# Error handling

If API call was not successful, additional information about problem can be found in

qualtrics.last_error_message - Human-readable error message (set to None is no error occurs)

qualtrics.json_response - python dictionary, JSON response returned by the server. May be None (if response is not a JSON document) 

qualtrics.last_url - URL constructed by the library

If maiformed response from Qualtrics is received, RuntimeError exception will be raised.

# License

You can use this under Apache 2.0. See LICENSE.txt file for details.

# Author

Alex Vyushkov, pyqualtrics[at]gmail.com

# Misc

Example JSON document returned by getLegacyResponseData

{
	u'R_syPqVCNJGCedrd7': {
		u'Status': u'0',
		u'StartDate': u'2015-10-2310: 59: 12',
		u'Q1': 2,
		u'Q2': 1,
		u'EndDate': u'2015-10-2310: 59: 23',
		u'Name': u'Freeborni,
		Anopheles',
		u'IPAddress': u'129.74.236.110',
		u'Q3': 2,
		u'ExternalDataReference': u'',
		u'Finished': u'1',
		u'EmailAddress': u'baguage+Freeborni@gmail.com',
		u'ResponseSet': u'DefaultResponseSet'
	}
}

Example output from getSurvey function

<?xml version="1.0" encoding="UTF-8"?>
<SurveyDefinition><SurveyName>Biting Habits</SurveyName><OwnerID>UR_2sExgmQSPbZHykt</OwnerID><isActive>1</isActive><CreationDate>2015-10-23 08:06:33</CreationDate><LastModifiedDate>2015-10-23 09:03:33</LastModifiedDate><StartDate>0000-00-00 00:00:00</StartDate><ExpirationDate>0000-00-00 00:00:00</ExpirationDate><Languages><Language Default="1">EN</Language></Languages><Questions><Question QuestionID="QID1"><Type>MC</Type><Selector>SAVR</Selector><SubSelector>TX</SubSelector><QuestionText><![CDATA[Did you bite a human inside of their house yestersday?]]></QuestionText><QuestionDescription><![CDATA[Did you bite a human inside of their house yestersday?]]></QuestionDescription><ExportTag><![CDATA[Q1]]></ExportTag><Validation><ForceResponse>0</ForceResponse></Validation><Choices><Choice ID="1" Recode="1"><Description><![CDATA[Yes]]></Description></Choice><Choice ID="2" Recode="2"><Description><![CDATA[No]]></Description></Choice></Choices></Question><Question QuestionID="QID2"><Type>MC</Type><Selector>SAVR</Selector><SubSelector>TX</SubSelector><QuestionText><![CDATA[Did you bite an animal yesterday?]]></QuestionText><QuestionDescription><![CDATA[Did you bite an animal yesterday?]]></QuestionDescription><ExportTag><![CDATA[Q2]]></ExportTag><Validation><ForceResponse>0</ForceResponse></Validation><Choices><Choice ID="1" Recode="1"><Description><![CDATA[Yes]]></Description></Choice><Choice ID="2" Recode="2"><Description><![CDATA[No]]></Description></Choice></Choices></Question><Question QuestionID="QID3"><Type>MC</Type><Selector>SAVR</Selector><SubSelector>TX</SubSelector><QuestionText><![CDATA[Did you bit a human outside of their house yesterday?]]></QuestionText><QuestionDescription><![CDATA[Did you bit a human outside of their house yesterday?]]></QuestionDescription><ExportTag><![CDATA[Q3]]></ExportTag><Validation><ForceResponse>0</ForceResponse></Validation><Choices><Choice ID="1" Recode="1"><Description><![CDATA[Yes]]></Description></Choice><Choice ID="2" Recode="2"><Description><![CDATA[No]]></Description></Choice></Choices></Question></Questions><Blocks><Block Description="Default Question Block" ID="BL_bjRmnCl7AUvhOfj"><BlockElements><Question QuestionID="QID1"/><Question QuestionID="QID2"/><Question QuestionID="QID3"/></BlockElements></Block></Blocks><SurveyFlow><Block FlowID="FL_2" ID="BL_bjRmnCl7AUvhOfj"/></SurveyFlow><EmbeddedData/></SurveyDefinition>

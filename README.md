# PyQualtrics

Unofficial python SDK for Qualtrics API

# Installation

Install using pip:

`pip install pyqualtrics`

Alternatively, you can download or clone this repo and call `pip install -e ..`

# How to run tests

# Usage example

This library requires account with Qualtrics API enabled. Check with your Qualtrics representative to see if API 
Access is available for your account. 

Please refer to http://www.qualtrics.com/university/researchsuite/developer-tools/api-integration/qualtrics-rest-api/ 
for information on how to get your API TOKEN and Qualtrics IDs.

```python
qualtrics = Qualtrics(QUALTRICS_USER, QUALTRICS_TOKEN)
responses = qualtrics.getLegacyResponseData(SurveyID=QUALTRICS_SURVEY_ID)
for response_id, response in response.itemitem():
    print response_id + " - " + response["Finished"]
```

# Documentation

Full documenation is available on wiki.

# Bugs and requests

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/Baguage/pyqualtrics/issues

# License

You can use this under Apache 2.0. See LICENSE.txt file for details.

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

[![Version](https://img.shields.io/pypi/v/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)
[![License](https://img.shields.io/pypi/l/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)
[![Python](https://img.shields.io/pypi/pyversions/pyqualtrics.svg)](https://pypi.python.org/pypi/pyqualtrics)

![Logo](img/pyqualtrics.png)

Unofficial python API for Qualtrics. 
-------------------
This library is intended to simplify integration of Qualtrics system with your python application, while preserving semantics of API when possible. You can automate survey or panel creation, automatically load survey responses to your system, use this library in your scripts and so on.

My ultimate goal is cover all API calls. Some of them (subscribe, createUser etc) require admin access, and I don't have it currently, so adding support for them may take a while. I do welcome pull requests if you'd like to contribute.

# System requirements

Python 2.7 only. I do intent to add support for Python 3.x in near future.

Requires setuptools. It might be already installed on your system, but if not you can use `ez_setup.py` script to install setuptools.

# Installation

Install the latest release using pip:

`pip install pyqualtrics`

Development version can installed using `pip install git+https://github.com/Baguage/pyqualtrics.git`

Alternatively, you can download or clone this repo and run `pip install -e ..`

# Configuration
This library requires account with Qualtrics API enabled. Check with your Qualtrics representative to see if API 
Access is available for your account.

Please refer to https://www.qualtrics.com/support/integrations/api-integration/api-integration/#GeneratingAnAPIToken 
for information on how to get your API Token and other Qualtrics IDs (in your Account Settings, 
click "Qualtrics Ids").


# Usage example

This is how you can get list of all responses to a survey (using API v2). 

```python
from pyqualtrics import Qualtrics

QUALTRICS_USER = "user@nd.edu#nd"
QUALTRICS_TOKEN = "lskdjfla93402930sldfkajlk32l4w3fsddsf"
QUALTRICS_SURVEY_ID = "SV_8pqqcl4sy2316ZF"

qualtrics = Qualtrics(QUALTRICS_USER, QUALTRICS_TOKEN)
responses = qualtrics.getLegacyResponseData(SurveyID=QUALTRICS_SURVEY_ID)
for response_id, response in responses.items():
    print response_id + " : " + response["Finished"]
```

getLegacyResponseData function returns an OrderedDict of all survey responses.

# Bugs and requests

Qualtrics support is awesome, but this is not official Qualtrics SDK and they DO NOT support this piece of software.
If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/Baguage/pyqualtrics/issues

# Error handling

If API call was not successful (return None or False), additional information about problem can be found in the following attributes of the Qualtrics object

`qualtrics.last_error_message` : Human-readable error message (set to None is no error occurs)

`qualtrics.response` : server response as a text string. Can be useful for debugging if server did not return JSON response for some reason

`qualtrics.r` : server response as a requests.Response object.

`qualtrics.json_response` : python dictionary, JSON response returned by the server. Can be None (if response is not a JSON document) 

`qualtrics.last_url` : URL constructed by the library (for both v3 and v2 API calls)

`qualtrics.last_data` : Body or last POST request (v3 calls only)

```python
from pyqualtrics import Qualtrics

qualtrics = Qualtrics(user="user", token="token")
xml = qualtrics.getSurvey(SurveyID="SV_8pqqcl4sy2316ZF")
if not xml:
   print "Error getting survey: %s" % qualtrics.last_error_message
```

# License

You can use this under Apache 2.0. See LICENSE.txt file for details. I appreciate if you drop me a line if you find this library useful!

# Author

Alex Vyushkov, pyqualtrics[at]gmail.com


Developer's notes
====

# API Documentation

The Qualtrics REST API allows you to query our system using a simple URL syntax. All requests are simple GET or POST requests that return XML or JSON.
Official API documenation is available on https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php

This library uses API v2.5

# How to run tests

Tests suite requires access to Qualtrics API. It uses following environment variables

QUALTRICS_USER	- Qualtrics User ID

QUALTRICS_TOKEN	- Token to access Qualtrics API

QUALTRICS_LIBRARY_ID - Library ID

Please refer to https://survey.qualtrics.com/WRAPI/ControlPanel/docs.php#authentication_2.5 for additional information
on how to get your API Token. Library ID can be found in the 'Qualtrics IDs' section.
If one of these variables is not defined, tests won't start at all.

If you want to run full test suite, you may want to create a survey, a message and one response in your Qualtrics account.
QUALTRICS_SURVEY_ID, QUALTRICS_RESPONSE_ID and QUALTRICS_MESSAGE_ID variable should be set to activate those tests

You can re-created Qualtrics survey used for testing using files in qualtrics_files_for_tests directory

# Notes for test_get_legacy_response_data test

This test requires a partially completed response in "getLegacyData test" survey (SV_8pqqcl4sy2316ZL), 
and it will closed after 6 month (max timeout allowed by Qualtrics). Thus every 6 month new 
partially completed response should be created. 

Use link https://nd.qualtrics.com/jfe/form/SV_8pqqcl4sy2316ZL and answer "Male". Don't answer the second question

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

from collections import OrderedDict


class MockQualtrics(object):
    """ Mock object for unit testing code that uses pyqualtrics library

    """
    def __init__(self, user=None, token=None, api_version="2.5"):
        self.user = user
        self.token = token
        self.api_version = api_version
        self.last_error_message = None
        self.last_url = None
        self.json_response = None
        self.response = None  # For debugging purpose
        self.mock_responses = OrderedDict()
        self.mock_responses_labels = OrderedDict()

    def getResponse(self, SurveyID, ResponseID, Labels=None, **kwargs):
        if Labels == "1":
            return self.mock_responses_labels.get(ResponseID, None)
        else:
            return self.mock_responses.get(ResponseID, None)

    def getLegacyResponseData(self, SurveyID, Labels=None, **kwargs):
        if Labels == "1":
            return self.mock_responses_labels
        else:
            return self.mock_responses

# Copyright 2016 Google Inc.
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

import webapp2
import random
import meditations
import config
from pymobius import Mobius
import json

# This will fix the pymobius requestor
import requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Init the mobius object
        mobius = Mobius(api_key=config.api_key)

        # Get the user's email and the api-key
        request_email = self.request.get_all("email")[0]
        request_api_key = self.request.get_all("api_key")[0]
        #request_email = self.request.get_all("email")[0].encode("utf-8")
        #request_api_key = self.request.get_all("api_key")[0].encode("utf-8")

        # Prep the response
        self.response.headers['Content-Type'] = 'text/plain'

        # Validate the api-key
        if (request_api_key == config.api_key):

            resp = mobius.app_store.use(app_uid=config.uid, email=request_email, num_credits=1)
            #resp = mobius.app_store.balance(app_uid=config.uid, email=request_email)

            quote = "Not enough tokens"

            if resp["success"]:
                quote = random.choice(meditations.quotes)

            to_write = {
                    "quote": quote,
                    "num_credits": resp["num_credits"]
                    }

            self.response.write(json.dumps(to_write))
        else:
            self.response.write("Invalid API Key")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

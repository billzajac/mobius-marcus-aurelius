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

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Init the mobius object
        mobius = Mobius(api_key=config.api_key)

        # Get the user's email and the api-key
        email = self.request.get_all("email")
        request_api_key = self.request.get_all("api_key")

        # Prep the response
        self.response.headers['Content-Type'] = 'text/plain'

        # Validate the api-key
        if (request_api_key == config.api_key):
            self.response.write("Invalid API Key")

        resp_json = mobius.app_store.use(app_uid=config.uid, email=email, num_credits=1)
        resp = json.loads(resp_json)

        if resp["success"]:
            self.response.write(random.choice(meditations.quotes))
        else:
            self.response.write("Not enough tokens")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

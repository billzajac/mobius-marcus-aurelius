# Copyright 2018 Bill Zajac
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import webapp2
import random
import meditations
import config
from pymobius import Mobius
import json

# This will fix the pymobius requestor
import requests
import requests_toolbelt.adapters.appengine
# Use the App Engine Requests adapter. This makes sure that Requests uses URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Prep the response
        self.response.headers['Content-Type'] = 'text/plain'

        # Get the user's email and the api-key
        request_email_params = self.request.get_all("email")
        request_api_key_params = self.request.get_all("api_key")

        # If there is no request_email or request_api_key, and request type is text/html
        if request_email_params == [] or request_api_key_params == []:
            error_msg = "USAGE: {}?email=EMAIL_TO_CHARGE&api_key=API_KEY_FOR_THIS_APP".format(self.request.url)
            self.response.write(error_msg)
            return

        request_email = request_email_params[0]
        request_api_key = request_api_key_params[0]

        # Init the mobius object
        mobius = Mobius(api_key=config.api_key)

        # Validate the api-key
        if request_api_key == config.api_key:

            try:
                resp = mobius.app_store.use(app_uid=config.uid, email=request_email, num_credits=config.credits_to_charge)
            except Exception as detail: 
                self.response.write(detail)
                self.response.write(" Possibly invalid email?")
                return

            quote = "Not enough tokens"

            if resp["success"]:
                quote = random.choice(meditations.quotes)

            to_write = {
                    "quote": quote,
                    "charged_credits": config.credits_to_charge,
                    "num_credits": resp["num_credits"]
                    }

            self.response.write(json.dumps(to_write))
        elif request_api_key == config.test_api_key: 
            resp = []
            try:
                resp = mobius.app_store.balance(app_uid=config.uid, email=request_email)
            except Exception as detail: 
                self.response.write(detail)
                self.response.write(" Possibly invalid email?")
                return

	    quote = random.choice(meditations.quotes)
            to_write = {
                    "quote": quote,
                    "charged_credits": "0.0",
                    "num_credits": resp["num_credits"]
                    }

            self.response.write(json.dumps(to_write))
        else:
            self.response.write("Invalid API Key")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

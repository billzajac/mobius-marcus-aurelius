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

        # Get the user's email and optionally the test key
        request_email_params = self.request.get_all("email")
        request_test_key_params = self.request.get_all("test_key")

        # If there is no request_email
        if request_email_params == []:
            error_msg = "USAGE: {}?email=EMAIL_TO_CHARGE".format(self.request.url)
            self.response.write(error_msg)
            return

        request_email = request_email_params[0]
        request_test_key = ""
        if len(request_test_key_params):
            request_test_key = request_test_key_params[0]

        # Init the mobius object
        mobius = Mobius(api_key=config.api_key)

        # Did we get the test_key?
        if request_test_key == config.test_key: 
            resp = []
            try:
                resp = mobius.app_store.balance(app_uid=config.uid, email=request_email)
            except Exception as detail: 
                self.response.write(detail)
                self.response.write(" Possibly invalid email?")
                return

	    # Always send the same quote for testing
	    quote = "When you arise in the morning, think of what a precious privilege it is to be alive - to breathe, to think, to enjoy, to love."
            to_write = {
                    "quote": quote,
                    "charged_credits": "0.0",
                    "num_credits": resp["num_credits"]
                    }

            self.response.write(json.dumps(to_write))
        else:
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

app = webapp2.WSGIApplication([
    ('/quote', MainPage),
    ('/quote/', MainPage),
], debug=True)

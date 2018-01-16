Blog Post
--------
* https://medium.com/@billzajac/mobius-with-python-and-google-appenine-68e0cf7e4060

Install
--------
* https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27
```
# pip2 install --upgrade pip setuptools # to upgrade pip
pip2 install -t lib -r requirements.txt

cp config.py.example to config.py
vi config.py
```

Test
--------
```
dev_appserver.py .
```

* Test without charging
    * Note: This will not charge and will use the API call 'balance' instead of 'use'
```
curl "localhost:8080?email=test@testing.com&api_key=YOUR_TEST_API_KEY"
```

* Example output
```
{"quote": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.", "num_credits": "4.0", "charged_credits": "0.0"}
```

* Test with an actual charge
```
curl "localhost:8080?email=test@testing.com&api_key=YOUR_API_KEY"
```

* Example output
```
{"quote": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.", "num_credits": "4.0", "charged_credits": "0.001"}
```

Deploy
--------
* https://cloud.google.com/appengine/docs/standard/python/getting-started/deploying-the-application
```
gcloud app deploy app.yaml
```

Mobius Testing
--------
```
curl -G "https://mobius.network/api/v1/app_store/balance" \
     -H "x-api-key: API_KEY_HERE" \
     -d "app_uid=APP_UID" \
     -d "email=EMAIL"
```

Notes
--------
* https://console.developers.google.com
* https://mobius.network/store/developer
* https://mobius.network/docs/?python#app-store

* https://github.com/zulucrypto/mobius-dapp-quickstart/blob/master/src/AppBundle/Controller/CoinFlipController.php

* https://mobius-marcus-aurelius.appspot.com
    * https://mobius-marcus-aurelius.appspot.com/static/marcus-aurelius.png


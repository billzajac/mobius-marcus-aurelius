Notes
--------
* https://console.developers.google.com
* https://mobius.network/store/developer
* https://mobius.network/docs/?python#app-store

* https://github.com/zulucrypto/mobius-dapp-quickstart/blob/master/src/AppBundle/Controller/CoinFlipController.php

* https://mobius-marcus-aurelius.appspot.com
    * https://mobius-marcus-aurelius.appspot.com/static/marcus-aurelius.png

Install
--------
* https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27
```
# pip2 install --upgrade pip setuptools
pip2 install -t lib -r requirements.txt
```

Test
--------
```
dev_appserver.py .
```

```
curl "localhost:8080?email=test@testing.com&api_key=YOUR_API_KEY"
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

import requests
myjson = {
    "client": {
      "clientId":      "ensimag_network_project",
      "clientVersion": "0.0.1"
    },
    "threatInfo": {
      "threatTypes":['THREAT_TYPE_UNSPECIFIED', 'MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
      "platformTypes":['ANY_PLATFORM'],
      "threatEntryTypes":['URL'],
      "threatEntries": [
        {"url": "cpcontacts.loveshackdiy.com"},
        {"url": "beta.servicehub.com"},
        {"url": "webmail.accantobeleza.com.br"},
        {"url": "www.1plus1.sk"},
        {"url": "www.raypal.com/"},
        {"url": "lefcm.org"},
        {"url": "forfriendsstore.com"},
        {"url": "api.atux.com.ar"},
        {"url": "www.mercercopywriting.co.uk"},
        {"url": "verkehrspsychologische-untersuchung-schweiz.online"},
        {"url": "bst-8b6d93ad-79da-40b9-8670-d837428ca3b1.bastion.azure.com"},
        {"url": "enterprisevineyards.com"},
        {"url": "wx.n3uc.com"},
        {"url": "vitalbites.us"},
        {"url": "labradortoscana.it"},
        {"url": "entizolab.com"},
        {"url": "www.hokkaido-select.com"},
        {"url": "www.jacklete.ca"},
        {"url": "46640.1602746166.cr-gke-boskos-40.cr-e2e.com"},
        {"url": "web-ssoreporting-test.apps.beta.azure.cp-skoda-auto.com"},
        {"url": "autodiscover.womanmoneyblog.com"}
      ]
    }
  }

# x = requests.get('https://w3schools.com/python/demopage.htm')
headers = {'Content-Type': 'application/json'}

api_key = 'AIzaSyBZUltwuT2ApyBvBi4Yr9BF5gQTNP7nwgI'

x = requests.post('https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + api_key, json=myjson, headers=headers)

print("text ", x.text) #print html content
try:
    print("json ", x.json)
except Exception:
    print("not in json")

# library to use it on github
# https://github.com/junv/safebrowsing/blob/master/safebrowsing.py

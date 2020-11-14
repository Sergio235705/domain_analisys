import json

import requests

# Age Of Domain <= 6 months -> Phishing
# Api : requestDataCreation allows to check the data Creation of domains
#

class dnstwisterAPI:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.api_adr = "https://dnstwister.report/api/whois/"
        self.api_toex = "https://dnstwister.report/api/to_hex/"

    def requestDataCreation(self, name):

        response = requests.get(self.api_toex + name )
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url = self.api_adr + response_dec)
        response = json.loads(response.text)
        response = response['whois_text']
        data_creation = response[response.find("Creation Date")+15:response.find("Creation Date")+25]
        return data_creation
"""
def main () :
    d = dnstwisterAPI()
    responde = d.request("amazon.com")
    print(responde)
if __name__ == "__main__":
    main()
"""


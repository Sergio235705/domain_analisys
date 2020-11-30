import json

import requests
import datetime
import re

# Age Of Domain <= 6 months -> Phishing
# Api : requestDataCreation allows to check the data Creation of domains
# Registry Expiry Date <= 1 year -> Phishing
# Registry Expiry Date - Creation Date <= 1 year -> Phishing
# Registry Registrant ID: REDACTED FOR PRIVACY -> Phishing
# Registrant Name: REDACTED FOR PRIVACY -> Phishing
# Registrant Organization: REDACTED FOR PRIVACY -> Phishing


class dnstwisterAPI:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.api_adr = "https://dnstwister.report/api/whois/"
        self.api_toex = "https://dnstwister.report/api/to_hex/"
        self.api_parked = "https://dnstwister.report/api/parked/"
        self.pattern_data = '([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'

    def numMonth(self , end, start):
        #print (end)
        #print(start)
        end_date = datetime.datetime(int(end[0:4]) , int(end[5:7]), int(end[8:]))
        start_date = datetime.datetime(int(start[0:4]), int(start[5:7]),int(start[8:]))

        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        #print(num_months)
        return num_months
    def validate(self,date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    def requestDateCreation(self, name):
        #print(name)
        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return {}
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        #print(response_dec)
        response = requests.get(url=self.api_adr + response_dec)
        if int(str(response)[11:14])!= 200:
            return {}
        response = json.loads(response.text)
        response = response['whois_text']
        data_creation = ""
        data_creation = response[response.find("Creation Date") + 15:response.find("Creation Date") + 25]
        if data_creation == "":
            return {}
        if self.validate(data_creation) is False:
            return {}
        return data_creation

    def requestExpiryDate(self, name):

        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return {}
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url=self.api_adr + response_dec)
        if int(str(response)[11:14])!= 200:
            return {}
        response = json.loads(response.text)
        response = response['whois_text']
        data_expiry = ""
        data_expiry = response[response.find("Registry Expiry Date") + 22:response.find("Registry Expiry Date") + 32]
        if data_expiry == "":
            return {}
        if self.validate(data_expiry) is False:
            return {}
        return data_expiry

    def requestRegistrantName(self, name):

        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return {}
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url=self.api_adr + response_dec)
        if int(str(response)[11:14])!= 200:
            return {}
        response = json.loads(response.text)
        name = ""
        response = response['whois_text']
        name = response[response.find("Registrant Name:") + 17:response.find("Registrant Name:") + 37]
        name = name.upper()
        if (name == "REDACTED FOR PRIVACY" or name == "WHOISPROTECTION.CC" or name == ""
            or "PRIVATE" in name or "WHOIS" in name or "PRIVACY" in name or "PROTECTED" in name or "PROTECTION" in name ):
            return {}
        return name


    def requestRegistrantOrganization(self, name):
        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return {}
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url=self.api_adr + response_dec)
        if int(str(response)[11:14])!= 200:
            return {}
        response = json.loads(response.text)
        name = ""
        response = response['whois_text']
        name = response[response.find("Registrant Organization:") + 25:response.find("Registrant Organization:") + 45]
        name = name.upper()
        if (name == "REDACTED FOR PRIVACY" or name == "WHOISPROTECTION.CC" or name == ""
                or "PRIVATE" in name or "PRIVACY" in name or "WHOIS" in name or "DOMAIN" in name) :
            return {}
        return name



    def requestRegistrarURL_Host(self, name):
        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return {}
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url=self.api_adr + response_dec)
        if int(str(response)[11:14])!= 200:
            return {}
        response = json.loads(response.text)
        name = ""
        response = response['whois_text']
        name = response[response.find("Registrar URL:") + 15:response.find("Registrar URL:") + 50]
        if name == "":
            return {}
        return name



    def requestParkedCheckUrl(self, name):
        response = requests.get(self.api_toex + name)
        if int(str(response)[11:14])!= 200:
            return float(0)
        response_dec = json.loads(response.text)
        response_dec = response_dec['domain_as_hexadecimal']
        response = requests.get(url=self.api_parked + response_dec)
        if int(str(response)[11:14])!= 200:
            return float(0)
        response = json.loads(response.text)
        score = response['score']  # > 0.50 good parameter -> possibly no phishing
        #print(score)
        return float(score)

"""
def main () :
    d = dnstwisterAPI()
    responde = d.requestXXXXXX("amazon.com")
    print(responde)
if __name__ == "__main__":
    main()
"""

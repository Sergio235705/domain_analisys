import requests

class SafebrowsingAPI:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}
        self.api_key = 'AIzaSyBZUltwuT2ApyBvBi4Yr9BF5gQTNP7nwgI'
        self.api_adr = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key

    def request(self, url):
        json_to_send = {
            "client": {
                "clientId": "ensimag_network_project",
                "clientVersion": "0.0.1"
            },
            "threatInfo": {
                "threatTypes":['THREAT_TYPE_UNSPECIFIED', 'MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
                "platformTypes":['ANY_PLATFORM'],
                "threatEntryTypes":['URL'],
                "threatEntries": [
                    {"url": url},
                ]
            }
        }
        response = requests.post(api_adr, json = json_to_send, headers = self.headers)
        return response.text


    def multiple_requests(self, url_list):
        json_to_send = {
            "client": {
                "clientId":      "ensimag_network_project",
                "clientVersion": "0.0.1"
            },
            "threatInfo": {
                "threatTypes":['THREAT_TYPE_UNSPECIFIED', 'MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
                "platformTypes":['ANY_PLATFORM'],
                "threatEntryTypes":['URL'],
                "threatEntries": [{"url": url} for url in url_list]
            }
        }
        response = requests.post(self.api_adr, json = json_to_send, headers = self.headers)
        return response.text

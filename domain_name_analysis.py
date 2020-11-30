import numpy as np
import dnstwisterAPI as dnstwisterAPI

import datetime


class Analyser():

    def split_name(self, url):
        """
        Splits an url between the name and the extension and removes the www if it exists
        Example: 'www.google.com' -> ('google', '.com')

        url: the url to split
        returns: tuple (name, extension)
        """
        url_splitted = url.split('.')
        extension = '.' + url_splitted.pop(-1)
        if (url_splitted[0] == 'www'):
            del url_splitted[0]
        name = '.'.join(url_splitted)
        return (name, extension)
    

    def __init__(self, url, authority):
        self.url = url
        if len(url) != 0:
            (self.name, self.extension) = self.split_name(self.url)
            if authority is not None:
                self.authority = authority.lower()
            else:
                self.authority = ""
            self.api = dnstwisterAPI.dnstwisterAPI(self.url)
        self.number_features = 16 # Number of feature we can compute

        # Taken from research paper / web-site ( https://security-soup.net/good-domains-for-bad-guys-the-riskiest-tlds-for-malware-and-phishing/)
        self.suspiciousTLDs = ['.bank', '.online', '.business', '.party', '.cc', '.pw', '.center', '.racing', '.cf',
                               '.ren', '.click', '.review', '.club', '.science', '.country', '.stream', '.download',
                               '.study', '.ga', '.support', '.gb', '.tech', '.gdn', '.tk', '.gq', '.top', '.info',
                               '.vip', '.kim', '.loan', '.work', '.men', '.win', '.ml', '.xyz', '.mom', '.xin',
                               '.jetzt', '.bid', '.ren', '.trade', '.date', '.wang', 'accountants', '.cricket', '.link',
                               '.rest', '.casa', '.tw', '.buzz', '.faith', '.ref', '.biz', '.tokyo', '.ooo',
                               '.yokohama', '.ryukyu', '.world', '.asia']

        # Original domain + country with +50M ppl
        self.nonSuspiciousTLDs = ['.com', '.org', '.net', '.eu', '.int', '.edu', '.gov', '.mil', '.cn', '.in', '.us',
                                  '.id', '.pk', '.br', '.ng', '.bd', '.ru', '.mx', '.jp', '.ph', '.cd', '.eg', '.et',
                                  '.vn', '.ir', '.tr', '.de', '.fr', '.uk', '.th', '.it', '.za', '.il', '.tz', '.mm',
                                  '.kr', '.co', '.tel', '.kw', '.jobs']

        self.suspicious_keywords_list = ['activity', 'office', 'appleid', 'outlook', 'poloniex', 'facebook',
                                         'moneygram', 'overstock', 'skype', 'alert', 'online', 'icloud', 'office365',
                                         'coinhive', 'tumblr', 'westernunion', 'alibaba', 'github', 'purchase',
                                         'recover', 'iforgot', 'microsoft', 'bithumb', 'reddit', 'bankofamerica',
                                         'aliexpress', 'authentication', 'safe', 'itunes', 'windows', 'kraken',
                                         'youtube', 'wellsfargo', 'leboncoin', 'authorize', 'secure', 'apple',
                                         'protonmail localbitcoin', 'twitter', 'paypal', 'amazon', 'netflix', 'bill',
                                         'security', 'tutanota', 'bitstamp', 'linkedin', 'citigroup', 'client',
                                         'service', 'hotmail', 'bittrex', 'instagram', 'santander support',
                                         'transaction', 'gmail', 'blockchain', 'flickr', 'morganstanley', 'unlock',
                                         'update', 'google', 'bitflyer', 'whatsapp', 'barclays', 'wallet', 'account',
                                         'outlook', 'coinbase', 'hsbc', 'form', 'login', 'yahoo', 'hitbtc', 'scottrade',
                                         'log-in', 'password', 'google', 'lakebtc', 'ameritrade', 'live', 'signin',
                                         'yandex', 'bitfinex', 'merilledge', 'manage', 'sign-in', 'bitconnect', 'bank',
                                         'verification', ' verify', 'coinsbank', 'webscr', 'invoice', 'authenticate',
                                         ' confirm', 'credential', 'customer', 'invoice', 'post', 'document', 'postal',
                                         'calculations', 'copy', 'fedex', 'statement', 'financial', 'dhl', 'usps',
                                         'notification', 'n', 'irs', 'ups', 'no', 'delivery', 'ticket', 'https', 'http',
                                         'auth', 'access', 'account', 'admin', 'agree', 'blue', 'business', 'cdn',
                                         'choose', 'claim', 'cl', 'click', 'confirm', 'confirmation', 'connect',
                                         'download', 'enroll', 'find', 'group', 'http', 'https', 'https-www', 'install',
                                         'login', 'mobile', 'mail', 'my', 'online', 'pay', 'payment', 'payments',
                                         'portal', 'recovery', 'register', 'ssl', 'safe', 'secure', 'security',
                                         'service', 'services', 'signin', 'signup', 'support', 'summary', 'update',
                                         'user', 'verify', 'verification', 'view', 'ww', 'www', 'web']

        self.suspicious_characters_list = ['@', '-']

        self.free_certificates_authorities = ["hubspot", "let's encrypt", "comodo", "cloudflare", "ssl for free",
                                              "godaddy", "geoTrust", "gogetssl", "instantssl", "basicssl", "zerossl",
                                              "certbot", "wosign", "free ssl space", "cacert", "startssl", "free ssl",
                                              "free ssl certificate", "gandi", "sectigo", "digicert",
                                              "wosign’s kuaissl"]
        self.suspicious_hosting = ["namecheap", "godaddy", "namesilo"]
    
    def levenshtein_distance(self, word):
        l1, l2 = len(self.name), len(word)
        d = np.zeros((l1 + 1, l2 + 1))
        subCost = 0

        for i in range(l1 + 1):
            d[i, 0] = i
        for j in range(l2 + 1):
            d[0, j] = j

        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                if self.name[i - 1] == word[j - 1]:
                    subCost = 0
                else:
                    subCost = 1
                d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + subCost)

        return int(d[l1, l2])

    def levenshtein(self):
        ld = []
        for word in self.suspicious_keywords_list:
            ld.append(self.levenshtein_distance(word))
        return min(ld)
        """
        Indicates if the certificate authority is a free certificate authority

        return: bool : true if certificate authority is free, false if not free
        """
    
    def issued_from_free_CA(self):
        res = False
        if self.authority == "":
            return res
            for ca in self.free_certificates_authorities:
                if ca in self.authority:
                    return res
        return res

    def deeply_nested_subdomains(self):
        """
        Give the number of '.' in the name which can be an indicator of suspiciousness if it is too high (F2 property)

        returns : nb of '.' in the name
        """
        return self.name.count('.')

    def suspicious_tld(self):
        """
        Say if the domain name is suspicious, not suspicious or unknown (F4 property)

        returns: 0 if unknown, 1 if non-suspicious, 2 if suspicious
        """

        if self.extension in self.suspiciousTLDs:
            return 2
        elif self.extension in self.nonSuspiciousTLDs:
            return 1
        else:
            return 0

    def inner_tld_in_subdomain(self):
        """
        Say if there is a domain name into the name, maybe to trick a user (F5 property)

        returns: True if there is at least one, False if not
        """

        for extension in self.nonSuspiciousTLDs:
            if extension in self.name:
                return 1
        return 0

    def suspicious_keywords(self):
        """
        Checks if there is suspicious keywordsin the name (F6 property)

        returns: ture if there is at least one
        """

        for keyword in self.suspicious_keywords_list:
            if keyword in self.name:
                if keyword == self.name:
                    # google.com isn't suspicious because there is google in the name
                    return 0
                else:
                    return 1
        return 0

    def hyphens_in_subdomain(self):
        """
        Give the number of "'" in the name which can be an indicator of suspiciousness if it is too high (F8 property)

        returns : nb of "'" in the name
        """
        return self.name.count("'")

    def suspicious_domain_length(self):
        """
        Analyse the length of the name which can be an indicator of suspiciousness if it is too high (F9 property)

        returns true if length is >= 54 ( Statistical analysis )
        """
        if len(self.name) >= 54:
            return 1
        else:
            return 0

    def suspicious_characters(self):
        """
        Checks if there is suspicious characters in the name (F10 property)

        returns: true if there is at least one
        """

        for ch in self.suspicious_characters_list:
            if ch in self.name:
                return 1
        return 0

    def suspicious_age_domain(self):
        """
        Checks if the domain age is suspicious (F11 property)
        dnstwister API
        Age Of Domain <= 6 months -> Phishing
        """
        today = datetime.date.today()
        d1 = today.strftime("%Y-%m-%d")
        #print("d1 =", d1)
        date = self.api.requestDateCreation()
        if date == {}:
            return True
        if self.api.numMonth(d1,date) > 6 :
            return False
        else :
            return True 

    def suspicious_date_creation(self):
        """
        date_creation in last month -> phishing 
        dnstwister API date = api.requestDateCreation(self.name+self.extension)
        """
        today = datetime.date.today()
        d1 = today.strftime("%Y-%m-%d")
        #print("d1 =", d1)
        date = self.api.requestDateCreation()
        if date == {}:
            return True
        if self.api.numMonth(d1,date) == 0 :
            return True
        else :
            return False 

    def suspicious_date_expiry(self):
        """
        Registry Expiry Date <= 1 year -> Phishing
        dnstwister API
        """
        today = datetime.date.today()
        d1 = today.strftime("%Y-%m-%d")
        #print("d1 =", d1)
        date = self.api.requestExpiryDate()
        if date == {}:
            return True
        if self.api.numMonth(d1,date) > 12 :
            return False
        else :
            return True 

    def suspicious_valid_period_domain(self):
        """
        Registry Expiry Date - Creation Date <= 1 year -> Phishing
        dnstwister API
        """
        

        dateEx = self.api.requestExpiryDate()
        dateCr = self.api.requestDateCreation()
        if dateEx == {} or dateCr == {}:
            return True
        if self.api.numMonth(dateEx,dateCr) > 12 :
            return False
        else :
            return True 

    def suspicious_registrant_name(self):
        """
        if Api.requestRegistrantName(self.name+self.extension) return {} is suspicious 
        dnstwister API
        """

        name = self.api.requestRegistrantName()
        if name == {}:
            return True
        return False
        

    def suspicious_registrant_organization(self):
        """
        if Api.requestRegistrantOrganization(self.name+self.extension) return {} is suspicious 
        dnstwister API
        """

        name = self.api.requestRegistrantOrganization()
        if name == {}:
            return True
        return False

    def suspicious_registrarURL(self):
        """
        if Api.requestRegistrantURL_Host(self.name+self.extension) return {} is suspicious 
        dnstwister API
        """

        name = self.api.requestRegistrarURL_Host()
        if name == {}:
            return True
        for host in self.suspicious_hosting:
            if host in self.name:
                return True
        return False

    def suspicious_parkerURL(self):
        """
       return requestParkedCheckUrl(self.name + self.extension) return score  ( > 0.50 good parameter -> possibly no phishing )
       dnstwister API
       """
       
        if (self.suspicious_age_domain() and   self.suspicious_date_creation() and self.suspicious_date_expiry() and self.suspicious_valid_period_domain()):
            value = self.api.requestParkedCheckUrl()
            if value > 0.50 :
                return False
            else:
                return True
        else:
          return False 

"""
1 Gaston
3 Morgane
2-4-5-6-8 Done here
7 to discuss with the teatcher
"""

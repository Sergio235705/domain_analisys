import numpy as np

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
        (self.name, self.extension) = self.split_name(self.url)
        self.authority = authority.lower();

        # Taken from research paper
        self.suspiciousTLDs = ['.bank', '.online', '.business', '.party', '.cc', '.pw', '.center', '.racing', '.cf', '.ren', '.click', '.review', '.club', '.science', '.country', '.stream', '.download', '.study', '.ga', '.support', '.gb', '.tech', '.gdn', '.tk', '.gq', '.top', '.info', '.vip', '.kim', '.win', '.loan', '.work', '.men', '.win', '.ml', '.xyz', '.mom']

        # Original domain + country with +50M ppl
        self.nonSuspiciousTLDs = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.cn', '.in', '.us', '.id', '.pk', '.br', '.ng', '.bd', '.ru', '.mx', '.jp', '.ph', '.cd', '.eg', '.et', '.vn', '.ir', '.tr', '.de', '.fr', '.uk', '.th', '.it', '.za', '.tz', '.mm', '.kr', '.co']

        self.suspicious_keywords_list = ['activity', 'office', 'appleid', 'outlook', 'poloniex', 'facebook', 'moneygram', 'overstock', 'skype', 'alert', 'online', 'icloud', 'office365', 'coinhive', 'tumblr', 'westernunion', 'alibaba', 'github', 'purchase', 'recover', 'iforgot', 'microsoft', 'bithumb', 'reddit', 'bankofamerica', 'aliexpress', 'authentication', 'safe', 'itunes', 'windows', 'kraken', 'youtube', 'wellsfargo', 'leboncoin', 'authorize', 'secure', 'apple', 'protonmail localbitcoin', 'twitter', 'paypal', 'amazon', 'netflix', 'bill', 'security', 'tutanota', 'bitstamp', 'linkedin', 'citigroup', 'client', 'service', 'hotmail', 'bittrex', 'instagram', 'santander support', 'transaction', 'gmail', 'blockchain', 'flickr', 'morganstanley', 'unlock', 'update', 'google', 'bitflyer', 'whatsapp', 'barclays', 'wallet', 'account', 'outlook', 'coinbase', 'hsbc', 'form', 'login', 'yahoo', 'hitbtc', 'scottrade', 'log-in', 'password', 'google', 'lakebtc', 'ameritrade', 'live', 'signin', 'yandex', 'bitfinex', 'merilledge', 'manage', 'sign-in', 'bitconnect', 'bank', 'verification', ' verify', 'coinsbank', 'webscr', 'invoice', 'authenticate', ' confirm', 'credential', 'customer']

        self.free_certificates_authorities = ["hubspot", "let's encrypt", "comodo", "cloudflare", "ssl for free", "godaddy", "geoTrust", "gogetssl", "instantssl", "basicssl", "zerossel", "certbot", "wosign", "free ssl space", "cacert", "startssl", "free ssl", "gandi", "sectigo", "digicert"]

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
                if self.name[i-1] == word[j-1]:
                    subCost = 0
                else:
                    subCost = 1
                d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + subCost)
        
        return int(d[l1, l2])

    def levenshtein(self):
        ld = []
        for word in self.suspicious_keywords_list:
            ld.append(self.levenshtein_distance(word))
        return min(ld)

    def issued_from_free_CA(self):
        """
        Indicates if the certificate authority is a free certificate authority

        return: bool : true if certificate authority is free, false if not free
        """
        res = False
        for ca in self.free_certificates_authorities:
            if ca in self.authority:
                res = True
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
                return True
        return False

    def suspicious_keywords(self):
        """
        Checks if there is suspicious keywordsin the name (F6 property)

        returns: ture if there is at least one
        """

        for keyword in self.suspicious_keywords_list:
            if keyword in self.name:
                if keyword == self.name:
                # google.com isn't suspicious because there is google in the name
                    return False
                else:
                    return True
        return False

    def hyphens_in_subdomain(self):
        """
        Give the number of "'" in the name which can be an indicator of suspiciousness if it is too high (F8 property)

        returns : nb of "'" in the name
        """
        return self.name.count("'")

"""
1 Gaston
3 Morgane
2-4-5-6-8 Done here
7 to discuss with the teatcher
"""

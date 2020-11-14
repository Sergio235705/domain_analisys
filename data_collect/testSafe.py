
from pysafebrowsing import SafeBrowsing

def main() :
    key = 'AIzaSyBZUltwuT2ApyBvBi4Yr9BF5gQTNP7nwgI'
    s = SafeBrowsing(key)
    url_list = ["malware.testing.google.test/testing/malware/","cpcontacts.loveshackdiy.com", "beta.servicehub.com",   "webmail.accantobeleza.com.br", "www.1plus1.sk",
                "www.raypal.com/", "lefcm.org", "forfriendsstore.com", "api.atux.com.ar", "www.mercercopywriting.co.uk",
                "verkehrspsychologische-untersuchung-schweiz.online",
                "bst-8b6d93ad-79da-40b9-8670-d837428ca3b1.bastion.azure.com", "enterprisevineyards.com", "wx.n3uc.com",
                "vitalbites.us", "labradortoscana.it", "entizolab.com", "www.hokkaido-select.com", "www.jacklete.ca",
                "46640.1602746166.cr-gke-boskos-40.cr-e2e.com",
                "web-ssoreporting-test.apps.beta.azure.cp-skoda-auto.com", "autodiscover.womanmoneyblog.com"]

    for r in url_list:
        h = s.lookup_url('http://'+r)
        print(h)

        #  example response : 
        # {'malicious': True, 'platforms': ['ANY_PLATFORM'], 'threats': ['MALWARE'], 'cache': '300s'}
        # {'malicious': False}


if __name__ == "__main__":
    main()
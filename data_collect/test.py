from safebrowsing_API import SafebrowsingAPI

my_API = SafebrowsingAPI()
url_list = ["cpcontacts.loveshackdiy.com", "beta.servicehub.com", "webmail.accantobeleza.com.br", "www.1plus1.sk", "www.raypal.com/", "lefcm.org", "forfriendsstore.com", "api.atux.com.ar", "www.mercercopywriting.co.uk", "verkehrspsychologische-untersuchung-schweiz.online", "bst-8b6d93ad-79da-40b9-8670-d837428ca3b1.bastion.azure.com", "enterprisevineyards.com", "wx.n3uc.com", "vitalbites.us", "labradortoscana.it", "entizolab.com", "www.hokkaido-select.com", "www.jacklete.ca", "46640.1602746166.cr-gke-boskos-40.cr-e2e.com", "web-ssoreporting-test.apps.beta.azure.cp-skoda-auto.com", "autodiscover.womanmoneyblog.com"]
print (my_API.multiple_requests(url_list))

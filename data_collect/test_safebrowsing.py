import safebrowsing

apikey = 'AIzaSyBZUltwuT2ApyBvBi4Yr9BF5gQTNP7nwgI'
sb = safebrowsing.LookupAPI(apikey)

def inspect (url):
    resp = sb.threat_matches_find(url)
    print(resp)

inspect('cpcontacts.loveshackdiy.com')
inspect('beta.servicehub.com')
inspect('webmail.accantobeleza.com.br')
inspect('www.1plus1.sk')
inspect('www.raypal.com/')
inspect('lefcm.org')
inspect('forfriendsstore.com')
inspect('api.atux.com.ar')
inspect('www.mercercopywriting.co.uk')
inspect('verkehrspsychologische-untersuchung-schweiz.online')
inspect('bst-8b6d93ad-79da-40b9-8670-d837428ca3b1.bastion.azure.com')
inspect('enterprisevineyards.com')
inspect('wx.n3uc.com')
inspect('vitalbites.us')
inspect('labradortoscana.it')
inspect('entizolab.com')
inspect('www.hokkaido-select.com')
inspect('www.jacklete.ca')
inspect('46640.1602746166.cr-gke-boskos-40.cr-e2e.com')
inspect('web-ssoreporting-test.apps.beta.azure.cp-skoda-auto.com')
inspect('autodiscover.womanmoneyblog.co')

class CertTreatment:
    def __init__(self, dict):
        self.content = dict

    def get_domain_name(self):
        return content['data']['leaf_cert']['all_domains'][0]

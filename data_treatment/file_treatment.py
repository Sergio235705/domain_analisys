import json
from cert_treatment import CertTreatment

class FileTreatment:
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.content = json.load(self.file)
        self.keys = list(self.dict.keys())
        self.nb_cert = len(self.keys)

    def get_nb_certificates(self):
        return self.nb_cert

    def annotate(self):
        for cert_name in self.keys:
            t = CertTreatment(self.content[cert_name])
            domain_name = t.get_domain_name()

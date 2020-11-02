from file_treatment import FileTreatment

a = FileTreatment('CertificateStream/test.json')
print(a.get_nb_certificates())
a.annotate()

Network project on the subject "CT logs and phishing"

How to use it:

Geneate a log file in json
    execute: python3 CertificateStream/certificate_file_generator.py file.json
    needs to be manually stopped (Ctrl-C) when you have enough certificates

Creation of a csv file with the results of googleSafeBrowsing API
    execute: python3 data_treatment/file_annotation.py file.json file.csv
    it uses my google account to perform the requests, don't make too much (limit near 10000/day)

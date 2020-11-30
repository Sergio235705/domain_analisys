class CertTreatment:
    def __init__(self, dict):
        self.content = dict

    def get_domain_name(self):
        return self.content['data']['leaf_cert']['all_domains'][0]

    def get_authority(self):
        return self.content['data']['chain'][0]['subject']['O']




"""
what a certificate looks like, you can use that to get the data you need to analyse
{
    "data": {
        "cert_index": 193451967,
        "cert_link": "http://ct.googleapis.com/logs/xenon2021/ct/v1/get-entries?start=193451967&end=193451967",
        "chain": [
            {
                "extensions": {
                    "authorityInfoAccess": "CA Issuers - URI:http://apps.identrust.com/roots/dstrootcax3.p7c\nOCSP - URI:http://isrg.trustid.ocsp.identrust.com\n",
                    "authorityKeyIdentifier": "keyid:C4:A7:B1:A4:7B:2C:71:FA:DB:E1:4B:90:75:FF:C4:15:60:85:89:10\n",
                    "basicConstraints": "CA:TRUE",
                    "certificatePolicies": "Policy: 1.3.6.1.4.1.44947.1.1.1\n  CPS: http://cps.root-x1.letsencrypt.org",
                    "crlDistributionPoints": "Full Name:\n URI:http://crl.identrust.com/DSTROOTCAX3CRL.crl",
                    "keyUsage": "Digital Signature, Key Cert Sign, C R L Sign",
                    "subjectKeyIdentifier": "A8:4A:6A:63:04:7D:DD:BA:E6:D1:39:B7:A6:45:65:EF:F3:A8:EC:A1"
                },
                "fingerprint": "E6:A3:B4:5B:06:2D:50:9B:33:82:28:2D:19:6E:FE:97:D5:95:6C:CB",
                "not_after": 1615999246,
                "not_before": 1458232846,
                "serial_number": "A0141420000015385736A0B85ECA708",
                "subject": {
                    "C": "US",
                    "CN": "Let's Encrypt Authority X3",
                    "L": null,
                    "O": "Let's Encrypt",
                    "OU": null,
                    "ST": null,
                    "aggregated": "/C=US/CN=Let's Encrypt Authority X3/O=Let's Encrypt"
                }
            },
            {
                "extensions": {
                    "basicConstraints": "CA:TRUE",
                    "keyUsage": "Key Cert Sign, C R L Sign",
                    "subjectKeyIdentifier": "C4:A7:B1:A4:7B:2C:71:FA:DB:E1:4B:90:75:FF:C4:15:60:85:89:10"
                },
                "fingerprint": "DA:C9:02:4F:54:D8:F6:DF:94:93:5F:B1:73:26:38:CA:6A:D7:7C:13",
                "not_after": 1633010475,
                "not_before": 970348339,
                "serial_number": "44AFB080D6A327BA893039862EF8406B",
                "subject": {
                    "C": null,
                    "CN": "DST Root CA X3",
                    "L": null,
                    "O": "Digital Signature Trust Co.",
                    "OU": null,
                    "ST": null,
                    "aggregated": "/CN=DST Root CA X3/O=Digital Signature Trust Co."
                }
            }
        ],
        "leaf_cert": {
            "all_domains": [
                "*.midwestcreditexpress.com",
                "midwestcreditexpress.com"
            ],
            "extensions": {
                "authorityInfoAccess": "CA Issuers - URI:http://cert.int-x3.letsencrypt.org/\nOCSP - URI:http://ocsp.int-x3.letsencrypt.org\n",
                "authorityKeyIdentifier": "keyid:A8:4A:6A:63:04:7D:DD:BA:E6:D1:39:B7:A6:45:65:EF:F3:A8:EC:A1\n",
                "basicConstraints": "CA:FALSE",
                "certificatePolicies": "Policy: 1.3.6.1.4.1.44947.1.1.1\n  CPS: http://cps.letsencrypt.org",
                "ctlPoisonByte": true,
                "extendedKeyUsage": "TLS Web server authentication, TLS Web client authentication",
                "keyUsage": "Digital Signature, Key Encipherment",
                "subjectAltName": "DNS:midwestcreditexpress.com, DNS:*.midwestcreditexpress.com",
                "subjectKeyIdentifier": "02:62:D2:5A:F0:80:D9:80:77:16:CD:9F:91:9E:B0:53:FA:29:F2:96"
            },
            "fingerprint": "F0:A0:21:FB:A6:D7:D3:AA:E7:37:A0:79:6F:EE:79:C1:C9:16:15:8B",
            "not_after": 1612365750,
            "not_before": 1604589750,
            "serial_number": "3A188580FF83480666D4629F2389A32637D",
            "subject": {
                "C": null,
                "CN": "midwestcreditexpress.com",
                "L": null,
                "O": null,
                "OU": null,
                "ST": null,
                "aggregated": "/CN=midwestcreditexpress.com"
            }
        },
        "seen": 1604593435.302594,
        "source": {
            "name": "Google 'Xenon2021' log",
            "url": "ct.googleapis.com/logs/xenon2021/"
        },
        "update_type": "PrecertLogEntry"
    },
    "message_type": "certificate_update"
}
"""

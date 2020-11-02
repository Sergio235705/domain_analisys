from domain_name_analysis import Analyser

def test(url):
    analyser = Analyser(url)
    result1 = analyser.suspicious_tld()
    result2 = analyser.inner_tld_in_subdomain()
    result3 = analyser.suspicious_keywords()

    result = ''
    if result1 == 0:
        result += 'unknown domain, '
    elif result1 == 1:
        result += 'non-suspicious domain, '
    elif result1 == 2:
        result += 'suspicious domain, '

    if result2:
        result += 'tld in the name, '
    else:
        result += 'no tld in the name, '

    if result3:
        result += 'suspicious_keyword detected'
    else:
        result += 'no suspicious_keyword detected'

    print(result)

if __name__ == '__main__':
    test('www.google.com')

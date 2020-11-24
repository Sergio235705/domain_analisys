import csv

def main():
    f = open('training_fake.csv', 'r')
    d = csv.DictReader(f)
    # r = d.__next__()
    # print (r)
    # print(r['domain_name'])
    for row in d:
        print(row)
        print(row["is_suspicious"])
        return  0

main()
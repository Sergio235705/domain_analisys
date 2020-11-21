import json
import logging
import datetime
import certstream
import sys
from pysafebrowsing import SafeBrowsing

global x , file 
def print_callback(message, context):
    global x, file
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

        x += 1
        print(x)
       # sys.stdout.write(
       #     u"{\"id\":})\n".format(x,datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), domain,
        #                                  ", ".join(message['data']['leaf_cert']['all_domains'][1:])))

      #  sys.stdout.write(
        #    u"({})[{}] {} (SAN: {})\n".format(x, datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), domain,
           #                                   ", ".join(message['data']['leaf_cert']['all_domains'][1:])))
        if x != 1 :
            file.write(", ")
        file.write("{ \"id\": "+"\""+str(x)+"\""+" , \"domain\": "+"\""+domain+"\" }")
        #print(domain)
        

       # sys.stdout.flush()

## Example   CaliMain.py  C:\Users\Sergio\Desktop\b.txt  1
def main():
    global x , file 
    x = 0
    name,nomeFile, minutes = sys.argv
    file = open(nomeFile,"w")
    file.write("[ ")
    
    logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)
    # implementation of this function is in core.py ( go to implementation )
    certstream.listen_for_events(print_callback,int(minutes), url='wss://certstream.calidog.io/')
    file.write(" ]")
    print("# certificates = " + str(x))
    res = int(x) / float(minutes)
    print("# certificates / minute = " + str(res))
    file.close()

if __name__ == "__main__":

    main()

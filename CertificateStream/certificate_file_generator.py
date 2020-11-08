import logging
import datetime
import certstream
import sys
import json
import os

def handle_callback(message, context):
    """
    function called to handle the information given by certstream
    """
    global json_file, current_cert

    #add cert to the file
    to_write = ''
    if json_file.tell() > 10:
        to_write += ', \n' # not to add the , on the first cert
    to_write += '"cert' + str(current_cert) + '": ' + into_json(message)
    json_file.write(to_write)

    # display the progress in the console
    if current_cert%100 == 0:
        print (current_cert, " certificates")

    current_cert += 1

def json_print(str):
    """
    takes a json string and print it properly
    """
    dict = json.loads(str)
    print(json.dumps(dict, indent = 4))

def into_json(src_dict):
    """
    takes a certificate given by the api and transforms it into proper json

    src_dict: the dictionnary from the CertStream API to transform
    returns: the string into proper json
    """
    cert_str = str(src_dict)
    cert_str = cert_str.replace('\n', '\\n')
    dst_dict = eval(cert_str)
    return json.dumps(dst_dict, indent=4)

def get_num_last_cert(file_path):
    """
    gives the number of the last cert in the given json file
    """
    if os.path.getsize(file_path) == 0:
        return -1

    file = open(file_path, "r")
    dict = json.load(file)
    keys = list(dict.keys())
    last_cert = keys[-1]
    num_last_cert = (int)(last_cert[4:])
    file.close()

    return num_last_cert

def main():
    # check if there is a given file
    if (len(sys.argv) != 2):
        print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("Missing an argument\nUsage: python3 certtest.py file.json")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        return -1

    global json_file, current_cert

    # delete the file if it exists
    try:
        f = open(sys.argv[1], "x") # raise an error if the file exists
        f.close()
    except:
        os.remove(sys.argv[1])
        f = open(sys.argv[1], "x")
        f.close()

    # open and intialize the file
    current_cert = 0
    json_file = open(sys.argv[1], "w")
    json_file.write('{')

    logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)
    certstream.listen_for_events(handle_callback, url='wss://certstream.calidog.io/')
    json_file.write('}')
    json_file.close()
    print("There are " + str(current_cert) + " certificates in the file")

if __name__ == "__main__":
    main()

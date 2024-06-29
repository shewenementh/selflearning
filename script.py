import os
import requests
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', action='store', dest='domains_file', required=True, help='File contins domains.')
parser.add_argument('-p', action='store', dest='PROT', default='https://', help='Protocol to use. i.e http://, https://')
arguments = parser.parse_args()

good_urls = []  # table for filtered urls
status_codes = {
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 300, 301, 302, 303, 304, 305, 307, 308,
    400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 
    421, 422, 423, 424, 425, 426, 428, 429, 431, 451, 500, 501, 502, 503, 504, 505, 506, 507, 
    508, 510, 511
}

os.makedirs(os.path.join(os.getcwd(), 'domainsFiles'), exist_ok=True)  # crete folder 'domainsFiles' in directory where the script is runing
os.chdir('domainsFiles') 

def replace_protocol(domain, new_protocol):# -p option in argparse
    if domain.startswith(("https://", "http://")):
        domain = re.sub(r'^https?:\/\/', new_protocol, domain)
    return domain

def urls(out_file, domains_file, PROT):
    # Read domains from file 
    with open(domains_file, 'r', encoding='utf-8') as file:  # tutaj bedzie podawany adres pliku
        domains = file.readlines()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    for domain in domains:
        domain = domain.strip()  
        if '://' not in domain:
            url = PROT + domain  
        else:
            url = replace_protocol(domain, PROT)

        try:
            response = requests.get(url, headers=headers)
            code =  response.status_code
            reson = response.reason
            inf = f"{code} {reson}\t{url}"
            if response.status_code in status_codes:
                good_urls.append(inf)

                # writing response headers to file 
                clean_filename = re.sub(r'[\/:*?"<>|]', '_', domain)
                with open(clean_filename + ".txt", 'w', encoding='utf-8') as new_file:
                    new_file.write(f"{code} {reson}""\n")
                    for key, value in response.headers.items():
                        new_file.write(f'{key}: {value}\n')
        
        except requests.exceptions.MissingSchema:
            continue
        except requests.exceptions.ConnectionError:
            continue

    # Saving filtered urls to file 
    with open(out_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(good_urls))

out_file = 'filtered_urls.txt'
urls(out_file, arguments.domains_file, arguments.PROT)


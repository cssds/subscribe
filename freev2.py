import urllib
# import requests,random,string
from datetime import datetime
import random
import requests
import string
import yaml

'''
"name":"feiniao",
"url":"https://feiniaoyun.xyz/",
"reg_url":"https://feiniaoyun.xyz/api/v1/passport/auth/register",
"sub":"https://feiniaoyun.xyz/api/v1/client/subscribe?token={token}"
'''

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}


class tempsite():
    def __init__(self, url, proxy=None):
        self._proxies = proxy
        self._name = ''
        self._url = url
        self._reg_url = ''
        self._sub = ''

    def set_env(self):
        self._name = urllib.parse.urlparse(self._url).netloc
        self._reg_url = self._url + 'api/v1/passport/auth/register'
        self._sub = self._url + 'api/v1/client/subscribe?token={token}'

    def register(self, email, password):
        headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            "Refer": self._url
        }
        data = {
            "email": email,
            "password": password,
            "invite_code": None,
            "email_code": None
        }
        req = requests.post(self._reg_url, headers=headers, data=data, timeout=5, proxies=self._proxies)
        return req

    def getSubscribe(self):
        password = ''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email = password + "@gmail.com"
        req = self.register(email, password)
        token = req.json()["data"]["token"]
        subscribe = self._sub.format(token=token)
        return subscribe

    def save_conf(self, currentTime):
        sub_url = self.getSubscribe()
        # retry
        for k in range(3):
            try:
                req = requests.get(sub_url, timeout=5)
                v2conf = req.text
                print(v2conf)
                headers = {
                    "User-Agent": 'ClashforWindows/0.20.10',
                    "Refer": self._url
                }
                clashConf = requests.get(sub_url, timeout=5,headers=headers).text
                print(clashConf)
                with open('./sub_list', 'a') as f:
                    f.write("[{}:] ".format(currentTime) + sub_url + '\n')
                with open('./infoClash', 'w') as f:
                    f.write(clashConf)
                with open('./info', 'w') as f:
                    f.write(v2conf)

                break
            except:
                v2conf = ""


def get_conf():
    currentTime = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")
    with open('./config.yaml', encoding="UTF-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    url_list = data['V2board']
    for url in url_list:
        sub = tempsite(url)
        try:
            sub.set_env()
            sub.save_conf(currentTime)
        except:
            pass

        # get_conf()

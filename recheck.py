import re
import requests
import threading
import time
import requests
from tqdm import tqdm
from retry import retry
from datetime import datetime


def sub_check(url, bar):
    headers = {'User-Agent': 'ClashforWindows/0.18.1'}
    with thread_max_num:
        @retry(tries=3)
        def start_check(url):
            res = requests.get(url, headers=headers, timeout=5)  # 设置5秒超时防止卡死
            if res.status_code == 200:
                try:  # 有流量信息
                    info = res.headers['subscription-userinfo']
                    info_num = re.findall('\d+', info)
                    time_now = int(time.time())
                    # 剩余流量大于10MB
                    if int(info_num[2]) - int(info_num[1]) - int(info_num[0]) > 10485760:
                        if len(info_num) == 4:  # 有时间信息
                            if time_now <= int(info_num[3]):  # 没有过期
                                new_list.append(url)
                            else:  # 已经过期
                                bin_list.append(url)
                        else:  # 没有时间信息
                            new_list.append(url)
                    else:  # 流量小于10MB
                        old_list.append(url)
                except:
                    old_list.append(url)
                    # output_text='无流量信息捏'
            else:
                bin_list.append(url)

        try:
            start_check(url)
        except:
            old_list.append(url)
        bar.update(1)


if __name__ == '__main__':
    new_list = []
    old_list = []
    bin_list = []
    with open('./logs/old/old', 'r') as f:
        data = f.read()
    url_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", data)  # 使用正则表达式查找订阅链接并创建列表
    # url_list = data.split() :list
    thread_max_num = threading.Semaphore(32)  # 32线程
    bar = tqdm(total=len(url_list), desc='漏网之鱼：')
    thread_list = []
    for url in url_list:
        # 为每个新URL创建线程
        t = threading.Thread(target=sub_check, args=(url, bar))
        # 加入线程池并启动
        thread_list.append(t)
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()
    bar.close()
    with open("./urllist", "a") as f:
        # str = '\n'
        # f.write(str.join(list))
        for url in new_list:
            f.write(url + '\n')
    with open("./logs/old/time", "w", encoding="UTF-8") as f:
        currentTime = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")
        f.write('更新时间:\t' + currentTime + '\n')

    with open('./urllist', 'r') as f:
        data = f.read()
    url_list = data.split()
    new_list = list(set(url_list))
    with open("./urllist", "w") as f:
        # str = '\n'
        # f.write(str.join(list))
        for url in new_list:
            f.write(url + '\n')
    
    with open('./logs/old/old', 'r') as f:
        data = f.read()
    url_list = data.split()
    old_list.extend(url_list)
    new_list = list(set(old_list))
    with open("./logs/old/old", "w") as f:
        # str = '\n'
        # f.write(str.join(list))
        for url in new_list:
            f.write(url + '\n')
            
    
    with open('./logs/old/bin', 'r') as f:
        data = f.read()
    url_list = data.split()
    bin_list.extend(url_list)
    new_list = list(set(bin_list))
    with open("./logs/old/bin", "w") as f:
        # str = '\n'
        # f.write(str.join(list))
        for url in new_list:
            f.write(url + '\n')

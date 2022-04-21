# encoding:utf-8
import requests
import httpx
import json
from bs4 import BeautifulSoup
import time
import csv
import random

requests = requests.session()  # 建立一个Session
year=input("请输入爬取当前年份")
mouth=input("请输入爬取月份")
cookitext = "SINAGLOBAL=9485957095805.742.1641285883325; _ga=GA1.2.1005456960.1646040583; UOR=,,www.baidu.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhuA1Az6n45pppnmj-1H1-j5JpX5KMhUgL.FoqR1Kq4eK501h52dJLoIEjLxKqL1-qLBoBLxKqL1KqL1KMLxK-LBKMLB.qLxKMLBKeL1K-f1K2c1h27; ALF=1681727484; SSOLoginState=1650191485; SCF=AjG8SWNI0eDf8jHIUXBv9bKNDy5bRS2IvHFqU5IHD_QSGpUf9jeDWiZ6hcuTFvyxqW3zKjM0zE9YKEeuIn47GUI.; SUB=_2A25PX5wuDeRhGeBG4lQY8S7PwzyIHXVsLIrmrDV8PUNbmtAfLRXzkW9NQfQ7NCHFnSV9q9voh2fJFIx752mEODbN; _s_tentry=login.sina.com.cn; Apache=6563696166481.694.1650191488468; ULV=1650191488473:9:5:1:6563696166481.694.1650191488468:1649998750003; webim_unReadCount=%7B%22time%22%3A1650191528028%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A20%2C%22msgbox%22%3A0%7D; XSRF-TOKEN=jqfG9TxFCpVxgUq6G9S2eZRi; WBPSESS=njN14ORccGwU3U136zmrS7QGuHHSNP86dm1PwVOTE-HOPYyKTG8LsZlEgEBWbQj8zB3YZGnb2TxPXunlL84bA0HHJgk8nguRolh_DU8G9fx0zxTsWoRuCiUIFXCdSPyjgbEyh-uihn_GbIsbP-WC9g==".replace('\n', '')
cookitext =input("请输入Cookie")
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookitext,
    'referer': 'https://weibo.com/2750621294/KAf1AFVPD',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-5b5f81f871c6ff6846bf3a92f1d5efed-1ab32a39ad75711a-00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': '7yIZGS_IPx7EteZ6TT86YYAZ',
}


def getWeiboCommentinfo(url):
    """
    主要是获取微博的信息，内容以及这个微博 MID UID,
    :param url:
    :return:
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookitext,
        'referer': 'https://www.baidu.com/link?url=79KIn7lPAsM1SqpiE6ub8unuDW2xwxX-4CyvQvA8HLS&wd=&eqid=dfbc01160004d2dc00000004619e5581',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.content, 'lxml')
    conetnt = html.find_all('div', class_="card-wrap")  # 这里CALSS 要加下划线
    for ct in conetnt:
        user_info = ct.find_all('a', class_="name")
        if user_info != []:
            try:
                mid = ct['mid']  # 获取微博ID
            except:
                pass
            else:
                user_name = user_info[0].text  # 用户名称
                uid = str(ct.find('div', class_="avator").find('a')['href']).split('/')[-1].split("?")[0]  # 获取UID
                user_index = "https:" + user_info[0]['href']  # 用户主页
                user_from = str(ct.find('p', class_="from").text).replace(' ', '').replace('\n', '')  # 时间和发布终端设备名称
                weibo_content = str(ct.find('p', class_="txt").text).replace(' ', '').replace('\n', '')  # 微博内容


                data = [weibo_content, user_name, user_from, user_index, mid, uid]

                max_id = 0
                htmlComment(data)
                getCommentLevel1(data, max_id)


def getCommentLevel1(data, max_id):
    """
    一级评论

    :return:
    """
    mid = data[-2]
    uid = data[-1]

    url = "https://weibo.com/ajax/statuses/buildComments?"

    par = {
        'id': mid,
        'is_show_bulletin': '2',
        'is_mix': '0',
        'max_id': max_id,
        'count': '20',
        'uid': uid,
    }
    client = httpx.Client(http2=True, verify=False)
    response = client.get(url, params=par, headers=headers)
    jsondata = json.loads(response.text)
    max_id = jsondata['max_id']  # 获取下一页mid
    content = jsondata['data']
    for ct in content:
        created_at = ct['created_at']  # 评论时间
        struct_time = time.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')  # 评论时间
        time_array = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 评论时间
        text = ct['text_raw']  # 评论内容
        screen_name = ct['user']['screen_name']  # 评论人名称
        weibo_comment_data = data + [text, time_array, screen_name]
        saveCsv(f"微博评论{year}年{mouth}月", weibo_comment_data)

    if max_id == 0:
        pass
    else:
        getCommentLevel1(data, max_id)


def htmlComment(data):

    mid = data[-2]
    uid = data[-1]
    url = 'https://s.weibo.com/Ajax_Comment/small?'
    par = {
        'act': 'list',
        'mid': mid,
        'uid': uid,
        'smartFlag': 'false',
        'smartCardComment': '',
        'isMain': 'true',
        'pageid': 'weibo',
        '_t': '0',
    }
    client = httpx.Client(http2=True, verify=False)
    response = client.get(url, params=par, headers=headers)
    jsondata = json.loads(response.text)['data']['html']
    html = BeautifulSoup(jsondata, 'lxml')
    comment_content = html.find_all('div', class_="content")
    for cc in comment_content:
        comment_info = str(cc.find('div', class_='txt').text).replace('\n', '').replace(' ', '').split('：')
        comment_text = comment_info[-1]
        comment_user = comment_info[0]
        comment_time = cc.find('p', class_="from").text
        weibo_comment_data = data + [comment_text, comment_time, comment_user]
        saveCsv(f"微博评论{year}年{mouth}月", weibo_comment_data)


def runx():
    # keytext = input('请输入关键词：')
    keytext = '新冠疫情'
    for day in range(1,29):
        for x in range(1, 3): #每天爬取多少页页的话题评论
            url = f"https://s.weibo.com/weibo?q={keytext}&timescope=custom:{int(year)-1}-12-31-0:{year}-{mouth}-{day}&page={x}"

            t = random.randint(2,5)
            print("当前爬取"+str(year)+"年第"+str(mouth)+"月第"+str(day)+"天第"+str(x)+"页评论数据")
            print(f"{t}秒后开始抓取")
            time.sleep(t)
            try:
                getWeiboCommentinfo(url)
            except Exception as e:
                print("爬取"+str(year)+"年第"+str(mouth)+"月第"+str(day)+"天第"+str(x)+"页评论数据时发生中断")
                print(e)


def saveCsv(filename, content):
    fp = open(f"{filename}.csv", 'a+', encoding='utf-8-sig', newline='')
    csv_fp = csv.writer(fp)
    csv_fp.writerow(content)
    fp.close()
    print(f"成功写入：{content}")


if __name__ == '__main__':
    runx()
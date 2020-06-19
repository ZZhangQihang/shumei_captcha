# -*- coding:utf-8 -*-

import re
import requests
from des import *
from image_match import *


def init_slider(referer_url):
    url = 'https://captcha.fengkongcloud.com/ca/v1/register'
    params = {
        'organization': 'eR46sBuqF0fdw7KWFLYa',
        'appId': 'default',
        'rversion': '1.0.1',
        'channel': 'web',
        'lang': 'zh-cn',
        'data': {},
        'model': 'slide',
        'callback': 'sm_{}'.format(int(time.time() * 1000)),
        'sdkver': '1.1.3'
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'captcha.fengkongcloud.com',
        'Pragma': 'no-cache',
        'Referer': referer_url,
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    response = requests.get(url=url, params=params, headers=headers, timeout=5)
    result = response.content.decode('utf-8')
    if re.findall(r'"riskLevel":"(.*?)",', result)[0] == 'PASS':
        return {
            'k': re.findall(r'"k":"(.*?)",', result)[0],
            'rid': re.findall(r'"rid":"(.*?)"', result)[0],
            'bg_url': 'https://castatic.fengkongcloud.com{}'.format(re.findall(r'"bg":"(.*?)",', result)[0]),
            'fg_url': 'https://castatic.fengkongcloud.com{}'.format(re.findall(r'"fg":"(.*?)",', result)[0])
        }


def get_des_data(init_data, distance, trace, times):
    key = decrypt('sshummei', base64.b64decode(init_data['k']))
    nw = str(encrypt(key, '-1'), encoding='utf-8')
    kw = str(encrypt(key, '200'), encoding='utf-8')
    be = str(encrypt(key, '1'), encoding='utf-8')
    zy = str(encrypt(key, str(distance / 400)), encoding='utf-8')
    ly = str(encrypt(key, 'zh-cn'), encoding='utf-8')
    bx = str(encrypt(key, 'web'), encoding='utf-8')
    ke = str(encrypt(key, '0'), encoding='utf-8')
    ik = str(encrypt(key, 'default'), encoding='utf-8')
    jr = str(encrypt(key, '400'), encoding='utf-8')
    dj = str(encrypt(key, str(times)), encoding='utf-8')
    wz = str(encrypt(key, str(trace)), encoding='utf-8')
    return {
        'nw': nw,
        'kw': kw,
        'be': be,
        'zy': zy,
        'ly': ly,
        'bx': bx,
        'ke': ke,
        'ik': ik,
        'jr': jr,
        'dj': dj,
        'rid': init_data['rid'],
        'wz': wz
    }


def verify_slider(data, referer_url):
    url = 'https://captcha.fengkongcloud.com/ca/v2/fverify'
    params = {
        'nw': data['nw'],
        'kw': data['kw'],
        'act.os': 'web_pc',
        'sdkver': '1.1.3',
        'be': data['be'],
        'zy': data['zy'],
        'ly': data['ly'],
        'bx': data['bx'],
        'ke': data['ke'],
        'ik': data['ik'],
        'callback': 'sm_{}'.format(int(time.time() * 1000)),
        'jr': data['jr'],
        'ostype': 'web',
        'organization': 'eR46sBuqF0fdw7KWFLYa',
        'rid': data['rid'],
        'dj': data['dj'],
        'rversion': '1.0.1',
        'protocol': '4',
        'wz': data['wz']
    }
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'captcha.fengkongcloud.com',
        'Pragma': 'no-cache',
        'Referer': referer_url,
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    response = requests.get(url=url, params=params, headers=headers, timeout=5)
    result = response.content.decode('utf-8')
    if re.findall(r'"riskLevel":"(.*?)"', result)[0] == 'PASS':
        print(result, '校验成功')
    else:
        print(result, '校验失败')


if __name__ == '__main__':
    for i in range(10):
        referer_url = 'https://www.xiaohongshu.com/web-login/captcha?redirectPath=https%3A%2F%2Fwww.xiaohongshu.com%2Fuser%2Fprofile%2F559ba95cf5a263177913fb00'
        init_data = init_slider(referer_url)
        distance = get_distance(init_data['bg_url'], init_data['fg_url'])
        trace, times = get_trace(distance)
        des_data = get_des_data(init_data, distance, trace, times)
        verify_slider(des_data, referer_url)

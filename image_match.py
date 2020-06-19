# -*- coding:utf-8 -*-

import ssl
import cv2
import time
import random
import numpy as np
from urllib.request import urlopen


def get_distance(fg, bg, resize_num=1):
    fg_obj = download_imdecode(src=fg)
    fg_gray = cv2.cvtColor(fg_obj, cv2.COLOR_BGR2GRAY)
    bg_obj = download_imdecode(bg, flag=0)
    res = cv2.matchTemplate(fg_gray, bg_obj, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(res)
    distance = max_indx[0] * resize_num
    return int(distance / 600 * 400)


def download_imdecode(src, flag=3):
    context = ssl._create_unverified_context()
    resp = urlopen(url=src, context=context)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, flag)
    return image


def get_trace(distance):
    start_time = int(time.time() * 1000)
    time.sleep(random.uniform(0.01, 0.05))
    back = random.randint(2, 6)
    distance += back
    v = 0
    tracks_list = []
    current = 0
    while current < distance - 13:
        a = random.randint(10000, 12000)  # 加速运动
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        current += s
        v = v0 + a * t / 1000
        if current < distance:
            tracks_list.append(round(current))
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    for _ in range(back):
        current -= 1
        tracks_list.append(round(current))
    tracks_list.append(round(current) - 1)
    if tracks_list[-1] != distance - back:
        tracks_list.append(distance - back)
    timestamp_list = []
    timestamp = int(time.time() * 1000)
    for i in range(len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    zy = 0
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
             0, -1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, -1, 0, 0])
        zy += y
        y_list.append(zy)
        j += 1
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([x, y_list[index], timestamp_list[index] - start_time])
    return trace, trace[-1][-1] + random.randint(1, 5)

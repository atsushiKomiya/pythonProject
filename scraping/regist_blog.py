#coding : utf-8

import math
import requests
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import os
import re
from PIL import Image
import io
from urllib import request
import chromedriver_binary
import csv
import re

FC2_URL = "https://admin.blog.fc2.com/control.php"
FC2_ID = "defxxxen@gmail.com"
FC2_PW = "w6c28fs54jq"

now = datetime.date.today()
year = now.year
month = now.month
day = now.day

# driver = webdriver.PhantomJS(executable_path='/Users/komiyaatsushi/Documents/phantomjs')

# ヘッドレス設定
# options = Options()
# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
# options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=options)

def login():
    id_input = driver.find_element_by_name("id")
    pw_input = driver.find_element_by_id("pass")
    # id_input = driver.find_elements_by_xpath('.//input[@name="email"]')

    id_input.send_keys(FC2_ID)
    pw_input.send_keys(FC2_PW)
    login_btn = driver.find_element_by_name("image")
    login_btn.click()

def access_new_blog():
    driver.find_element_by_class_name("gtm-lm_editor").click()

def get_category(merker):

    if merker.count('シロウト'):
        return 2
    elif merker.count('ラグジュ'):
        return 3
    elif merker.count('ナンパ'):
        return 5
    elif merker.count('ドキュメン'):
        return 6
    elif merker.count('募集ちゃん'):
        return 8
    elif merker.count('街行くセレブ'):
        return 9
    elif merker.count('家まで送ってイイですか'):
        return 10
    elif merker.count('屈辱の'):
        return 11
    elif merker.count('プレステージ'):
        return 12
    elif merker.count('プレステージプレミアム(PRESTIGE PREMIUM)'):
        return 13
    elif merker.count('ARA'):
        return 14
    elif merker.count('DOC'):
        return 15
    elif merker.count('KANBi'):
        return 16
    elif merker.count('MAD'):
        return 17
    elif merker.count('MAXING'):
        return 18
    elif merker.count('MBM'):
        return 19
    elif merker.count('SODクリエイト'):
        return 20
    elif merker.count('SODマジックミラー'):
        return 21
    elif merker.count('エチケット'):
        return 22
    elif merker.count('オフパコ'):
        return 23
    elif merker.count('ゲッツ!!'):
        return 24
    elif merker.count('なまなま.net'):
        return 25
    elif merker.count('ハメドリネットワーク2nd'):
        return 26
    elif merker.count('ビッグモーカル'):
        return 27
    elif merker.count('ファーストスター'):
        return 28
    elif merker.count('プラネットプラス'):
        return 29
    elif merker.count('マーキュリー'):
        return 30
    elif merker.count('人妻花園劇場'):
        return 31
    elif merker.count('投稿マーケット素人イッてQ'):
        return 32
    else:
        return 0


def input_blog(row, html, title, merker):

    html_data = html.read()

    category = get_category(merker)

    try:
        driver.find_element_by_css_selector('#change_normal_link img').click()
        # html_btn = d.find_element_by_css_selector('.trumbowyg-viewHTML-button')
        # html_btn = driver.find_element_by_link_text("HTML表示")
        # d.find_element_by_class_name("trumbowyg-viewHTML-button").click()
    except Exception as e:
        print('not #change_normal_link link')

    try:
        select_category = driver.find_element_by_name("entry[category]")
        category_opt = Select(select_category)
        category_opt.select_by_value(str(category))

        title_input = driver.find_element_by_name("entry[title]")
        title_input.send_keys(title)
        body_input = driver.find_element_by_name("entry[body]")
        body_input.send_keys(html_data)

        theme_select = driver.find_element_by_id("cate3")
        theme_opt = Select(theme_select)
        theme_opt.select_by_value(str('28978'))

        time.sleep(1)
        save_btn = driver.find_element_by_class_name('save_btn')
        save_btn.click()
        time.sleep(1)

    except Exception as e:
        print('except2')
        print(e)

# main
if __name__ == '__main__':
    
    try:
        # ブラウザ起動
        driver = webdriver.Chrome(executable_path='/Users/komiyaatsushi/Documents/chromedriver')
        # options = Options()
        # options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        # # options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=options)

        driver.get(FC2_URL)
        time.sleep(1)

        login()
        time.sleep(1)
        access_new_blog()

        file = open('./csv/upload.' + str(year) + str(month) + str(day) + '.csv')
        f = csv.reader(file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        for row in f:
            time.sleep(1)
            prod_no = row[4]
            title = row[0]
            prod_no = re.search(r'品番： *([!-~]*)', prod_no).group(1)
            merker = row[2][6:]
            html_path = "./source/" + str(prod_no) + '.html'
            html_for_title = open(html_path, "r", encoding="utf-8")
            html = open(html_path, "r", encoding="utf-8")
            input_blog(row, html, title, merker)

            time.sleep(1)

            html_for_title.close()
            html.close()
            time.sleep(1)
            access_new_blog()
            
        
        file.close()
        time.sleep(1)

    except Exception as e:
        print(str(e))
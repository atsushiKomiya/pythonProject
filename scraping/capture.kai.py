import math
import requests
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import os
import re
from PIL import Image
import io
from urllib import request
import chromedriver_binary
from selenium.webdriver.support.ui import Select

#　作品読み込み総数
ARRIVAL_GET_COUNT = 100
# テスト用に検索開始時のオフセット値
OFFSET_NO = 0
# サンプル画像取得件数 メイン画像含むため 11 
IMG_GET_COUNT = 11

# def get_sample_movie_code(driver):

#     try:
#         driver.find_element_by_class_name("button_aff_sample").click()
#         time.sleep(1)
#         player_size_select = driver.find_element_by_id("player_size")
#         player_size_opt = Select(player_size_select)
#         player_size_opt.select_by_value('99')
#         time.sleep(1)
#         sample_movie_tag = driver.find_element_by_id('pc_tag')
#         print(sample_movie_tag)
#     except Exception as e:
#         print(e)
    
#     # print(player_size_select)


def set_csv_format(target, title):

    range_cnt = len(target)

    target_text = ''
    target_list = {}
    title = title.text.replace(",", "")
    target_list[0] = title
    # 0 はタイトルが入るため 1 スタート
    for ino in range(range_cnt):

        if target[ino].text.count('出演'):
            target_list[1] = target[ino].text
        else:
            if 1 not in target_list:
                target_list[1] = '出演： '

        if target[ino].text.count('メーカー'):
            target_list[2] = target[ino].text
        else:
            if 2 not in target_list:
                target_list[2] = 'メーカー： '

        if target[ino].text.count('収録時間'):
            target_list[3] = target[ino].text
        else:
            if 3 not in target_list:
                target_list[3] = '収録時間： '

        if target[ino].text.count('品番'):
            target_list[4] = target[ino].text
        else:
            if 4 not in target_list:
                target_list[4] = '品番： '

        if target[ino].text.count('配信開始日'):
            target_list[5] = target[ino].text
        else:
            if 5 not in target_list:
                target_list[5] = '配信開始日： '

        if target[ino].text.count('商品発売日'):
            target_list[6] = target[ino].text
        else:
            if 6 not in target_list:
                target_list[6] = '商品発売日： '

        if target[ino].text.count('シリーズ'):
            target_list[7] = target[ino].text
        else:
            if 7 not in target_list:
                target_list[7] = 'シリーズ： '

        if target[ino].text.count('レーベル'):
            target_list[8] = target[ino].text
        else:
            if 8 not in target_list:
                target_list[8] = 'レーベル： '

        if target[ino].text.count('ジャンル'):
            target_list[9] = target[ino].text
        else:
            if 9 not in target_list:
                target_list[9] = 'ジャンル： '

        if target[ino].text.count('対応デバイス'):
            target_list[10] = target[ino].text
        else:
            if 10 not in target_list:
                target_list[10] = '対応デバイス： '

    for row in target_list.values():
        target_text += row.replace(",", "") + "\n"
        
    return target_text

def enable_download_in_headless_chrome(browser, download_dir):
    #add missing support for chrome "send_command"  to selenium webdriver
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# 抽出対象外判定 対象外なら True
def check_excluded(text):

    if (text.count('熟女') is True or text.count('貧乳') is True
        or text.count('ブス') is True
        or text.count('デブ') is True
    ):
        return True
    else:
        return False

if __name__ == '__main__':

    try:

        # 最新作ページ
        URL = 'https://www.mgstage.com/search/search.php?search_word=&sort=new&list_cnt=120&disp_type=thumb&search_range=latest'

        # Chromeで操作する場合
        # driver = webdriver.Chrome(executable_path='/Users/komiyaatsushi/Documents/chromedriver')
        # Chrome headless
        options = Options()
        options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        # ページをロード
        driver.get(URL)

        now = datetime.date.today()

        new_dir_path = './images_path/' + str(now.year) + str(now.month)
        if os.path.exists(new_dir_path) is not True:
            os.makedirs(new_dir_path)
            os.chmod(new_dir_path, 777)

        # headress でもダウンロードができるように
        # enable_download_in_headless_chrome(driver, new_dir_path )

        # ID名：custom_html-2　の要素を取得
        # tag_id = driver.find_element_by_id(ID_NAME)
        file = open('./csv/upload.' + str(now.year) + str(now.month) + str(now.day) + '.csv', 'w')

        target_tag = driver.find_element_by_id('AC')
        target_tag.click()
        # time.sleep(200)
        # target = driver.find_element_by_class_name("rank_list")


        # for i in range(120):
        for i in range(ARRIVAL_GET_COUNT):

            prod_img_dir = new_dir_path
            path = '//*[@class="rank_list"]/ul/li/a'
            # print(path)
            target = driver.find_elements_by_xpath(path)

            try:
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                target[i+OFFSET_NO].click()
            except Exception as e:
                print('list index out of range???')
                print(e)
                target_tag = driver.find_element_by_id('AC')
                target_tag.click()
                target = driver.find_elements_by_xpath(path)
                target[i+OFFSET_NO].click()

            time.sleep(1)

            # ここから各商品詳細ページ

            # sample_movie_code = get_sample_movie_code(driver)

            # 商品説明詳細部
            try:
                detail_data_elm = driver.find_element_by_class_name("detail_data")
            except Exception as e:
                print('no class detail_data')
                print(e)

            prod_detail_text = detail_data_elm.text
            # 抽出対象外 キーワード
            if check_excluded(prod_detail_text):
                print('continue')
                continue

            # 品番取得
            prod_no = re.search(r'品番： *([!-~]*)', prod_detail_text).group(1)
            print(prod_no)

            # 画像保存ディレクトリ作成
            prod_img_dir = prod_img_dir + '/' + str(prod_no)

            if os.path.exists(prod_img_dir) is not True:
                os.makedirs(prod_img_dir)
            else:
                # 画像ディレクトリが既にあるものは、以前に取り込んでいるため対象外
                driver.back()
                continue

            # メイン画像取得
            try:
                driver.find_element_by_xpath('//div/h2/img').click()
                time.sleep(2)
                main_img_url = driver.find_element_by_id("lightbox-image").get_attribute("src")
                # f = io.BytesIO(request.urlopen(main_img_url).read())
                # img = Image.open(f)
                # if img.mode != "RGB":
                #     # RGBモードに変換する
                #     img = img.convert("RGB")
                #     img.save(prod_img_dir + '/main.jpg')
                # else:
                #     img.save(prod_img_dir + '/main.jpg')
                # driver.find_element_by_id("lightbox-secNav-btnClose").click()
                f = open(prod_img_dir + '/images.url', 'a')
                f.write(main_img_url + "\r")
                # driver.find_element_by_id("jquery-overlay").click()
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element_by_id("lightbox-secNav-btnClose").click()

            except Exception as e:
                print('main img get error')
                print(e)
            
            time.sleep(1)
            # ・・・すべてを見る クリック
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element_by_xpath("//p[@id='introduction_all']/a").click()
            except Exception as e:
                print('not more link.')
                print(e)

            # 商品紹介文
            introduction = driver.find_element_by_class_name("introduction")

            photos_dl = driver.find_element_by_id('sample-photo')

            # 画像ダウンロード
            sample_photos = photos_dl.find_elements_by_xpath(".//ul/li/a")
            img_cnt = 0
            photo_cnt = len(sample_photos)
            for ind in range(photo_cnt):

                # 画像ダウンロードは１２個まで (メイン画像含む)
                if img_cnt >= IMG_GET_COUNT:
                    break

                try:
                    time.sleep(1)
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sample_photos[ind].click()
                    except Exception as e:
                        print('sample_photos[ind] error')
                        print(e)

                    time.sleep(1)
                    img_elm = driver.find_element_by_id("lightbox-image")
                    img_url = img_elm.get_attribute("src")
                    # f = io.BytesIO(request.urlopen(img_url).read())
                    # img = Image.open(f)
                    # if img.mode != "RGB":
                    #     # RGBモードに変換する
                    #     img = img.convert("RGB")
                    #     img.save(prod_img_dir + '/{}.jpg'.format(ind))
                    # else:
                    #     img.save(prod_img_dir + '/{}.jpg'.format(ind))
                    f = open(prod_img_dir + '/images.url', 'a')
                    f.write(img_url + "\r")

                    time.sleep(0.3)
                    # driver.find_element_by_id("jquery-overlay").click()
                    driver.find_element_by_id("lightbox-secNav-btnClose").click()
                    time.sleep(0.7)
                except Exception as e:
                    print('except1')
                    print(e)

                img_cnt += 1

            # target_txt_list = target.text.rsplit("： ", 1)
            # pattern = "(.*)画像を拡大する(.*)"
            # target.text = re.search(pattern, target.text)
            target_text = ''
            title = driver.find_element_by_xpath("//h1[@class='tag']")
            if (prod_no.count('SIRO')):
                print("SIRO")
                element = driver.find_elements_by_xpath("//div[@class='detail_data']/table/tbody/tr")
            else:
                print("ETC")
                element = driver.find_element_by_class_name("detail_data")
                element = element.find_elements_by_xpath("//table[2]/tbody/tr")
                if len(element) == 0:
                    element = driver.find_element_by_class_name("detail_data")
                    element = element.find_elements_by_xpath("//table/tbody/tr")

            try:
                target_text = set_csv_format(element, title)

            except Exception as e:
                print('except2')
                print(e)
                
            target_text += introduction.text
            replace_text = target_text.replace(",", "")
            file.write(replace_text.replace("\n", ",") + "\n")

            driver.back()
            # 戻るじゃなく、直にURLへ移動
            # driver.get(URL)
            time.sleep(2)

        driver.close()
        driver.quit()
        file.close()

        print('Success!')

    except Exception as e:
        print('main Exception')
        print(e)
#coding : utf-8

import math
import requests
import time
import datetime
import os
import io
import re
import csv
import shutil
import glob

AFFILIATE_CODE = '~AFGAJ3XJUP64UYWZY8TUALGAWBIJ'
MGS_URL = 'http://www.mgstage.com/'
MGS_AFF_URL = MGS_URL + AFFILIATE_CODE + '/product/product_detail/{}'

MGS_JS_TAG = 'https://www.mgstage.com/js/mgs_sample_movie.js?p={}&r=1&c=GAJ3XJUP64UYWZY8TUALGAWBIJ'

FC2_FTP_IMG_PATH = "https://file.blog.fc2.com/xxxde01xxx/"

now = datetime.date.today()
year = now.year
month = now.month
day = now.day

filename = './csv/upload.' + str(year) + str(month) + str(day) + '.csv'
img_dir_path = './images/' + str(year) + str(month)

def listup_files(path):
    # yield [os.path.abspath(p) for p in glob.glob(path)]
    return glob.glob(path)

def get_csv():

    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            data.append(row)
    
    return data

def create_html(list):


    for ind, rows in enumerate(list):
        try:

            prod_no = rows[4]
            prod_no = re.search(r'品番： *([!-~]*)', prod_no).group(1)

            target_img_dir_path = str(img_dir_path) + '/' + str(prod_no)

            # template.html をコピー
            regist_file = './source/' + str(prod_no) + '.html'
            template_file = './template.html'
            shutil.copyfile(template_file, regist_file)
            # コピーファイル開き、内容変更する

            # #with openでファイルを開いて、勝手に閉じてくれる。
            with open(regist_file,"r+",encoding="utf-8") as file:
                filedata=file.read()

                # #replaceでPublishという文字列をDraftという文字列に置換してくれる。

                # # "w"とwriteでは中身が全て上書きされる。
                with open(regist_file,"w",encoding="utf-8") as file:

                    filedata=filedata.replace("HEAD_TITLE", rows[0])
                    filedata=filedata.replace("MGS_JS_TAG", MGS_JS_TAG.format(prod_no))
                    filedata=filedata.replace("MGS_AFF_URL", MGS_AFF_URL.format(prod_no))
                    filedata=filedata.replace("TITLE", rows[0])

                    # サンプル画像リンクタグ作成
                    main_img_tag = ''
                    imgs_tag = ''
                    img_list = listup_files(target_img_dir_path + '/./*')
                    img_list.sort()
                    for img in img_list:
                        img = img[2:]
                        img = FC2_FTP_IMG_PATH + img
                        if img.count('main.jpg'):
                            main_img_tag = """
<a href="{}" target="_blank">
    <img src="{}" alt="pb_e_200gana-1283.jpg" border="0" width="840" height="472">
</a>
                            """.format(img, img)
                            continue

                        imgs_tag += """
<a href="{}" target="_blank">
    <img src="{}" alt="pb_e_200gana-1283.jpg" border="0" width="840" height="472">
</a>
                        """.format(img, img)
                    filedata=filedata.replace("MAIN_IMG", main_img_tag)
                    filedata=filedata.replace("IMAGES", imgs_tag)

                    # 商品詳細タグ作成
                    performer = rows[1].split('： ')
                    merker = rows[2].split('： ')
                    duration = rows[3].split('： ')
                    product_code = rows[4].split('： ')
                    distribution_start_date = rows[5].split('： ')
                    release_date = rows[6].split('： ')
                    series = rows[7].split('： ')
                    label = rows[8].split('： ')
                    genre = rows[9].split('： ')
                    enabled_device = rows[10].split('： ')

                    details_tag = ""
                    for i in range(10):

                        if i == 0 or i == 1:
                            continue

                        detail_dict = rows[i].split('： ')
                        details_tag += """
    <tr>
        <th>{}</th><td>{}</td>
    </tr>
                        """.format(detail_dict[0] + str("："), detail_dict[1] if len(detail_dict) > 1 else '')

                    filedata=filedata.replace('DETAILS', details_tag)

                    # 商品説明文
                    introduction = rows[11]
                    filedata=filedata.replace('INTRODUCTION', introduction)

                    file.write(filedata)

        except Exception as e:
            print('except1')
            print(e)
            # 何かしらのエラーの場合は、次回、再取得対象にするため画像ディレクトリ削除
            # if os.path.exists(target_img_dir_path) is True:
            #     shutil.rmtree(target_img_dir_path)

# main
if __name__ == '__main__':
    
    try:

        post_list = get_csv()
        create_html(post_list)
        

    except Exception as e:
        print(str(e))
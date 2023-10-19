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
import ftplib
from ftplib import FTP

hostname = "ftp.blog.fc2.com"
username = "xxxde01xxx"
password = "w6c28fs54jq"

now = datetime.date.today()
year = now.year
month = now.month
day = now.day

img_dir_path = './images/' + str(year) + str(month)

def ftp_upload(upload_src_path, upload_dst_path):
    # FTP接続・アップロード

    # login
    ftp = ftplib.FTP(hostname)
    ftp.set_pasv("true")
    ftp.login(username, password)

    dirs = upload_src_path.split('/')
    print(upload_src_path)
    # ディレクトリ存在確認
    try:
        ftp.mkd(dirs[0] + "/" + dirs[1])
    except:
        print('except1')
        # ./images/ ディレクトリは作成済み

    try:
        ftp.mkd(dirs[0] + "/" + dirs[1] + "/" + dirs[2])
    except:
        print('except2')
        # ./images/YYYYM/ は作成済み

    try:
        ftp.mkd(dirs[0] + "/" + dirs[1] + "/" + dirs[2] + "/" + dirs[3])
    except:
        print('except3')
        # ./images/YYYYM/PROD_NO は作成済み

    fp = open(upload_src_path, "rb")
    ftp.storbinary(str("STOR ") + upload_src_path ,fp)

    # 終了処理
    ftp.close()
    fp.close()

def listup_files(path):
    # yield [os.path.abspath(p) for p in glob.glob(path)]
    return glob.glob(path)

# main
if __name__ == '__main__':
    
    try:
        file = open('./csv/upload.' + str(year) + str(month) + str(day) + '.csv')
        f = csv.reader(file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        for row in f:
            prod_no = row[4]
            prod_no = re.search(r'品番： *([!-~]*)', prod_no).group(1)
            img_dir_list = listup_files(img_dir_path + "/" + str(prod_no) + "/*")
            for img_path in img_dir_list:
                try:
                    ftp_upload(img_path, img_path)

                    # TODO エラーがなければローカルの画像ファイルを削除する？
                    # dirs = upload_src_path.split('/')

                except:
                    print('except0')

    except Exception as e:
        print(str(e))
# -*- coding: utf-8 -*-
#スクレイピングに必要なモジュール
import requests
from bs4 import BeautifulSoup
#モジュールインポート
import sitelist

import time #sleep用
import sys  #エラー検知用
import re   #正規表現
import csv  #csv操作
import numpy    #csv操作

with open('result.csv', 'a', encoding="utf_8_sig") as csv_file:
    fieldnames = ['Ranks','Horse_Name','Jockey','Age','M/F']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

for scraping_sitename in sitelist.SITE_URL:

    #攻撃とみなされないように時間を置く
    time.sleep(3)
    try:
        # スクレイピング対象の URL にリクエストを送り HTML を取得する
        res = requests.get(scraping_sitename)

        res.raise_for_status()  #URLが正しくない場合，例外を発生させる

        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.content, 'html.parser')

        # title タグの文字列を取得する
        title_text = soup.find('title').get_text()
        print(title_text)

        #順位のリスト作成
        Ranks = soup.find_all('div', class_='Rank')
        Ranks_list = []
        for Rank in Ranks:
            Rank = Rank.get_text()
            #リスト作成
            Ranks_list.append(Rank)
        print(Ranks_list)   #debug


        #馬名取得
        Horse_Names = soup.find_all('span', class_='Horse_Name')
        Horse_Names_list = []
        for Horse_Name in Horse_Names:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Horse_Name = Horse_Name.get_text().lstrip().rstrip('\n')
            #リスト作成
            Horse_Names_list.append(Horse_Name)
        print(Horse_Names_list) #debug


        #騎手名取得
        Jockey_Names = soup.find_all('td', class_='Jockey')
        Jockey_Names_list = []
        for Jockey_Name in Jockey_Names:
            #馬名のみ取得(lstrip()先頭の空白削除，rstrip()改行削除)
            Jockey_Name = Jockey_Name.get_text().lstrip().rstrip('\n').strip('☆').strip('△')
            #リスト作成
            Jockey_Names_list.append(Jockey_Name)
        print(Jockey_Names_list) #debug
        
        #性齢取得
        Age = soup.find_all('span', class_='Lgt_Txt Txt_C')
        Age_list = []
        for Age in Age:
            Age = Age.get_text().lstrip().rstrip('\n').strip('牡').strip('牝')
            Age_list.append(Age)
        print(Age_list)
      
        Mf = soup.find_all('span', class_='Lgt_Txt Txt_C')
        Mf_list = []
        for Mf in Mf:
            Mf = Mf.get_text().lstrip().rstrip('\n').rstrip('2').rstrip('3').rstrip('4').rstrip('5').rstrip('6').rstrip('7').rstrip('8')
            Mf_list.append(Mf)
        print(Mf_list)
        """
        #人気取得
        Ninkis = soup.find_all('span', class_='OddsPeople')
        Ninkis_list = []
        for Ninki in Ninkis:
            Ninki = Ninki.get_text()
            #リスト作成
            Ninkis_list.append(Ninki)
        print(Ninkis_list)  #debug

        #枠取得
        Wakus = soup.find_all('td', class_="Waku1 Txt_C")
        Wakus_list = []
        for Waku in Wakus:
            Waku = Waku.get_text().replace('\n','')
            #リスト作成
            Wakus_list.append(Waku)
        print(Wakus_list)

        #コース,距離取得
        Distance_Course = soup.find_all('span')
        Distance_Course = re.search(r'.[0-9]+m', str(Distance_Course))
        Course = Distance_Course.group()[0]
        Distance = re.sub("\\D", "", Distance_Course.group())
        print(Course)   #debug
        print(Distance) #debug
        """

        with open('result.csv', 'a', encoding="utf_8_sig") as csv_file:
            fieldnames = ['Ranks_list','Horse_Name','Jockey_Names','Age','Mf']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            #writer.writeheader()
            #順位-馬名-人気のリスト作成(CSVへ書き込み)
            for Ranks_list,Horse_Name_list,Jockey_Names_list,Age_list,Mf_list in zip(Ranks_list,Horse_Names_list,Jockey_Names_list,Age_list,Mf_list):
                print(Ranks_list,Horse_Name_list,Jockey_Names_list,Age_list,Mf_list)
                writer.writerow({'Horse_Name': Horse_Name_list,'Ranks_list': Ranks_list,'Jockey_Names': Jockey_Names_list,'Age': Age_list,'Mf':Mf_list})


    except:
        print(sys.exc_info())
        print("サイト取得エラー")
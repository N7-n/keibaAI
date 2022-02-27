# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

import sitelist

import sqlite3

import time 
import sys  
import re    


con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

for scraping_sitename in sitelist.SITE_URL:
    time.sleep(3)
    try:
        res = requests.get(scraping_sitename)

        res.raise_for_status() 

        soup = BeautifulSoup(res.content, 'html.parser')

        # title取得
        title_text = soup.find('title').get_text()

        #順位取得
        Ranks = soup.find_all('div', class_='Rank')
        Ranks_list = []
        for Rank in Ranks:
            Rank = Rank.get_text()
  
            Ranks_list.append(Rank)

        #馬名取得
        Horse_Names = soup.find_all('span', class_='Horse_Name')
        Horse_Names_list = []
        for Horse_Name in Horse_Names:
            #lstrip()先頭の空白削除，rstrip()改行削除
            Horse_Name = Horse_Name.get_text().lstrip().rstrip('\n')

            Horse_Names_list.append(Horse_Name)

        #騎手名取得
        Jockey_Names = soup.find_all('td', class_='Jockey')
        Jockey_Names_list = []
        for Jockey_Name in Jockey_Names:

            Jockey_Name = Jockey_Name.get_text().lstrip().rstrip('\n').strip('☆').strip('△')

            Jockey_Names_list.append(Jockey_Name)
        
        #馬齢取得
        Age = soup.find_all('span', class_='Lgt_Txt Txt_C')
        Age_list = []
        for Age in Age:
            Age = Age.get_text().lstrip().rstrip('\n').strip('牡').strip('牝').strip('セ')
            Age_list.append(Age)

        #性別取得
        Mf = soup.find_all('span', class_='Lgt_Txt Txt_C')
        Mf_list = []
        for Mf in Mf:
            Mf = Mf.get_text().lstrip().rstrip('\n').rstrip('2').rstrip('3').rstrip('4').rstrip('5').rstrip('6').rstrip('7').rstrip('8')
            Mf_list.append(Mf)
        #データベースへの書き込み
        for Ranks_list,Horse_Names_list,Jockey_Names_list,Age_list,Mf_list in zip(Ranks_list,Horse_Names_list,Jockey_Names_list,Age_list,Mf_list):
            print(Ranks_list,Horse_Names_list,Jockey_Names_list,Age_list,Mf_list)
            cur.execute('INSERT INTO data values(?,?,?,?,?)',[str(Ranks_list),str(Horse_Names_list) , str(Jockey_Names_list),int(Age_list),str(Mf_list)])
            con.commit()

    except:
        print(sys.exc_info())
        print("サイト取得エラー")
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Score import Score

from bs4 import BeautifulSoup
from selenium import webdriver

import os
import re

folderDict = {
    "1":"01_1st_style",
    "s":"01_substream",
    "2":"02_2nd_style",
    "3":"03_3rd_style",
    "4":"04_4th_style",
    "5":"05_5th_style",
    "6":"06_6th_style",
    "7":"07_7th_style",
    "8":"08_8th_style",
    "9":"09_9th_style",
    "10":"10_10th_style",
    "11":"11_IIDX_RED",
    "12":"12_HAPPY_SKY",
    "13":"13_DistorteD",
    "14":"14_GOLD",
    "15":"15_DJ_TROOPERS",
    "16":"16_EMPRESS",
    "17":"17_SIRIUS",
    "18":"18_Resort_Anthem",
    "19":"19_Lincle",
    "20":"20_tricoro",
    "21":"21_SPADA",
    "22":"22_PENDUAL",
    "23":"23_copula",
    "24":"24_SINOBUZ",
    "25":"25_CANNON_BALLERS",
    "26":"26_Rootage",
}

def main():
    if not os.path.exists(os.getcwd()+'/scores'):
        os.makedirs(os.getcwd()+'/scores')
    if not os.path.exists(os.getcwd()+'/scores/SP'):
        os.makedirs(os.getcwd()+'/scores/SP')
        
    score=Score()
    
    ver_url_list = ["http://textage.cc/score/?vQ11B00"]
    for ver_url in ver_url_list:
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver',chrome_options=options)
        driver.get(ver_url)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "lxml")
        url_list=[]
        songs = soup.center.find_all('table')[1].tbody.find_all('tr')[1:]
        for song in songs:
            try:
                url = song.find_all('td')[0].find_all('a')[0].get('href')
                url_list.append("http://textage.cc/score/"+url)
            except:
                pass
                
        for url_ in url_list:
            try:
                url=re.findall(r'([^/\.\?]+)', url_)
                if not os.path.exists(os.getcwd()+'/scores/SP/'+folderDict[url[-4]]):
                    os.makedirs(os.getcwd()+'/scores/SP/'+folderDict[url[-4]])
                    
                fileName=folderDict[url[-4]]+'/'+url[-3]+'_'+re.findall(r'([A-Z1-9])',url[-1])[1]+'.txt'
                if not os.path.exists('scores/SP/'+fileName):
                    score.analyze_web(url_)
                    score.save_text(os.getcwd()+'/scores/SP/'+fileName)
                    print(fileName)
            except:
                pass


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import kokontouzai, ayame, elephant, potitto, morikinoko,  esuesugame, ssbiyori, horaizoon, ssnavi, ssimas, sslog, esuesu, sshouko, maniax
import pprint
import os

functions = {'古今東西': ('kokontouzai', kokontouzai)
            , 'ポチッと':('potitto', potitto)
             , '森きのこ':('morikinoko', morikinoko)
             , 'えすえすゲー':('ssgame', esuesugame)
             , 'SSびより':('ssbiyori', ssbiyori)
             , 'ホライゾーン':('horizoon', horaizoon)
             , 'SSなび':('ssnavi', ssnavi)
             , 'あやめ':('ayame', ayame)
             , 'エレファント':('elephant', elephant)
             , 'アイマス':('imas', ssimas)
             , 'SSログ':('sslog', sslog)
             , 'えすえす':('ss', esuesu)
             , '宝庫':('sshouko', sshouko)
             , 'まにあっくす':('esusokuhou', maniax)}


def get_title():
    print('Please input title from under list...')
    pprint.pprint(functions.keys())
    while True:
        name = input('>')
        if name in functions.keys():
            return name

if __name__=='__main__':
    key = get_title()
    name = functions[key][0]
    function = functions[key][1]
    save_dir = os.path.join('/home/maya/PycharmProjects/TextScraping/Datasets2', name+'_raw')
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    function.call(save_dir)
    
    
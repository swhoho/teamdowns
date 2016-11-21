#두번쨰 파일입니다. 몽고DB로 데이터를 저장하는 파일입니다. 
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')





from collections import Counter
import numpy as np
import pandas as pd
from pymongo import MongoClient
from operator import itemgetter
from bs4 import BeautifulSoup
import requests
import json
import re
from pymongo import MongoClient


class Href_to_data(object):
    def __init__(self):
        pass
        
    def href_to_mongodb(self):
        mongo = MongoClient('127.0.0.1', 27017)
        hrefbase = mongo.Hrefs.urls
        house_info = mongo.dabang.room_db2
        ls = set() 
        try:
            for i in house_info.find():
                ls.add('https://www.dabangapp.com/room/'+ i['id'])
        except:
            ls = []
        
        house_data = [] 
        for  href in  hrefbase.find():
            if href['url'] in ls:
                continue
            try:
                web = requests.get(href['url'])
                x = re.search('dabang.web.detail\((.*}})',web.content) 
                jsonform = x.group(1)
            except:continue
            try:
                jsonf = json.loads(jsonform)
            except:continue
            housedict = {}
            housedict['id'] = jsonf['room']['id']
            housedict['address']= jsonf['room']['address']
            housedict['loc'] = (jsonf['room']['location'])
            housedict['room_size'] = jsonf['room']['room_size']
            housedict['room_floor'] = jsonf['room']['room_floor']
            housedict['building_floor'] = jsonf['room']['building_floor']
            housedict['room_options'] = jsonf['room']['room_options']
            housedict['room_type'] = jsonf['room']['room_type_str']
            try:
                housedict['metro_count'] = jsonf['room']['near'][0]['total']
                housedict['d_to_metro'] = min(jsonf['room']['near'][0]['pois'],key = itemgetter('distance'))['distance']
                housedict['d_to_conv'] = min(jsonf['room']['near'][1]['pois'],key = itemgetter('distance'))['distance']
                housedict['d_to_coffe'] = min(jsonf['room']['near'][2]['pois'],key = itemgetter('distance'))['distance']
                housedict['d_to_bank'] = min(jsonf['room']['near'][3]['pois'],key = itemgetter('distance'))['distance']
            except:
                print 'fail'
                housedict['metro_count'] = np.nan
                housedict['d_to_metro'] = np.nan
                housedict['d_to_conv'] = np.nan
                housedict['d_to_coffe'] = np.nan
                housedict['d_to_bank']= np.nan
	    
            try:
                housedict['elevator'],housedict['parking'],housedict['animal'] = jsonf['room']['elevator'],jsonf['room']['parking'],jsonf['room']['animal']
            except:
                housedict['elevator'],housedict['parking'] = np.nan, np.nan
            try:
                if jsonf['room']['maintenance']:
                    mc = jsonf['room']['maintenance_cost']
                else: 
                    mc = 0
                if mc is None: 
                    mc = 0
                deposit = jsonf['room']['price_info'][0][0] 
                if deposit is None: 
                    deposit = 0
                rent = jsonf['room']['price_info'][0][1] 
                if rent is None :
                    rent = 0
                price = deposit + (rent + mc) * 100
            except:continue
            housedict['price'] = price
            try:
                house_info.insert_one(housedict)
                print 'Success'
            except: 
                print 'fail'
                continue


                
if __name__ == '__main__':                
    print 'start'    
    data = Href_to_data()
    data.href_to_mongodb()
    print 'Suceesfully insert data '

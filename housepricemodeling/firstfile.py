from selenium.webdriver.support.ui import Select
from  pyvirtualdisplay import Display
import time
from pymongo import MongoClient
from selenium import webdriver
from collections import Counter

class HREF_SCRETCHER_DABANG(object):
    
    def __init__(self, dong_lst):
        dong_lst = [i.strip() for i in dong_lst] 
        self.dong_lst = dong_lst
    
   
    
    def extract_href(self):
        href_lst = []
        display = Display(visible=0, size=(800,600))
        display.start()
        driver = webdriver.Chrome()
        driver.get('''https://www.dabangapp.com/search#/map?type=region&id=11140162&position=%7B%22center%22%3A%5B127.01550714548125%2C37.55690177250604%5D%2C%22zoom%22%3A14%7D&filters=%7B%22deposit-range%22%3A%5B0%2C999999%5D%2C%22price-range%22%3A%5B0%2C999999%5D%2C%22room-type%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%5D%2C%22deal-type%22%3A%5B0%2C1%5D%2C%22location%22%3A%5B%5B126.97662584360137%2C37.537813508505565%5D%2C%5B127.05438844736113%2C37.57598514804419%5D%5D%7D&cluster=%7B%22name%22%3A%22%EC%8B%A0%EB%8B%B9%EB%8F%99%22%7D''')
        for i in self.dong_lst:
            try:
                text_box = driver.find_element_by_xpath("//input[@class='SearchForm-input form-control']")
                text_box.clear()
                address =  i
                address = address.decode('utf8')
                text_box.send_keys(address)
                time.sleep(5)
            except:continue
            try:
                click_box = driver.find_element_by_xpath('''//ul[@class='SearchForm-list search-items']/li/span[@class='SearchForm-item name full']''')
                text = click_box.text
            except:
                print 'text_error' 
            if address in text:    
                click_box.click() 
            else:
                print 'not match'
                continue    
            time.sleep(3)
            try:
                region_box = driver.find_elements_by_class_name("Room-item")
                for i,room_info in enumerate(region_box):
                    try:
                        link = room_info.find_element_by_tag_name('a')
                        href = link.get_attribute('href')
                        href_lst.append(href)
                    except:
                        print 'no a tag with href'
                
                        
                while True:
                    try:
                        time.sleep(3)
                        next_icon = driver.find_element_by_xpath("//ul[@class='Pagination']//a[@class='Pagination-item Pagination-item--next']")
                        next_icon.click()
                        region_box = driver.find_elements_by_class_name("Room-item")
                        for i,room_info in enumerate(region_box):
                            try:
                                link = room_info.find_element_by_tag_name('a')
                                href = link.get_attribute('href')
                                href_lst.append(href)
                            except:
                                print 'no a tag with href'
                                continue
                        
                    except: 
                        print 'no next icon'
                        break

                    
            
            except:
                print 'Nothing to do'
        driver.quit()
        return href_lst
    
    def extract_final_lst(self):
        href_lst = self.extract_href()
        href_dict = Counter(href_lst)
        final_lst = href_dict.keys()
        self.final_lst = final_lst
        return final_lst
    
    def href_to_mongo(self):
        mongo = MongoClient('127.0.0.1', 27017)
        database = mongo.Hrefs.urls
        href_data = []
        st = set()
        for i in database.find():
            st.add(i['url'])
        for i in self.final_lst:
            url = {}
            if i in st:
                continue
            url['url'] = i
            href_data.append(url)
        database.insert_many(href_data)
    def write_file(self, file_name):
        with open(file_name,'w') as txtfile:
            for i in self.final_lst:
                url = i + ' '
                txtfile.write(url)


if __name__ == '__main__':
    print 'start'
    u_lst = ['\xec\x84\x9c\xec\x9a\xb8\xea\xb5\x90\xec\x9c\xa1\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xec\x9a\xb8\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xec\x9a\xb8\xea\xb3\xbc\xed\x95\x99\xea\xb8\xb0\xec\x88\xa0\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xea\xb5\xad\xeb\xb0\xa9\xec\x86\xa1\xed\x86\xb5\xec\x8b\xa0\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xea\xb5\xad\xec\xb2\xb4\xec\x9c\xa1\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xec\x9a\xb8\xec\x8b\x9c\xeb\xa6\xbd\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb0\x80\xed\x86\xa8\xeb\xa6\xad\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb0\x90\xeb\xa6\xac\xea\xb5\x90\xec\x8b\xa0\xed\x95\x99\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb1\xb4\xea\xb5\xad\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb2\xbd\xea\xb8\xb0\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb2\xbd\xed\x9d\xac\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb3\xa0\xeb\xa0\xa4\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb4\x91\xec\x9a\xb4\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb5\xad\xeb\xaf\xbc\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xea\xb7\xb8\xeb\xa6\xac\xec\x8a\xa4\xeb\x8f\x84\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xeb\x8d\x95\xec\x84\xb1\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xeb\x8f\x99\xea\xb5\xad\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xeb\x8f\x99\xeb\x8d\x95\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xeb\xaa\x85\xec\xa7\x80\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x82\xbc\xec\x9c\xa1\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x83\x81\xeb\xaa\x85\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xea\xb0\x95\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xea\xb2\xbd\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xec\x9a\xb8\xea\xb8\xb0\xeb\x8f\x85\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\x9c\xec\x9a\xb8\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\xb1\xea\xb3\xb5\xed\x9a\x8c\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\xb1\xea\xb7\xa0\xea\xb4\x80\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\xb1\xec\x8b\xa0\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x84\xb8\xec\xa2\x85\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x88\x99\xeb\xaa\x85\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x88\xad\xec\x8b\xa4\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x97\xb0\xec\x84\xb8\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x9d\xb4\xed\x99\x94\xec\x97\xac\xec\x9e\x90\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\x9e\xa5\xeb\xa1\x9c\xed\x9a\x8c\xec\x8b\xa0\xed\x95\x99\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\xa4\x91\xec\x95\x99\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\xb4\x9d\xec\x8b\xa0\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xec\xb6\x94\xea\xb3\x84\xec\x98\x88\xec\x88\xa0\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xea\xb5\xad\xec\x84\xb1\xec\x84\x9c\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xea\xb5\xad\xec\x99\xb8\xea\xb5\xad\xec\x96\xb4\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xec\x84\xb1\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xec\x96\x91\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x95\x9c\xec\x98\x81\xec\x8b\xa0\xed\x95\x99\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90', '\xed\x99\x8d\xec\x9d\xb5\xeb\x8c\x80\xed\x95\x99\xea\xb5\x90']
    dabang =HREF_SCRETCHER_DABANG(u_lst)
    dabang.extract_final_lst()
    dabang.href_to_mongo()
    print 'Sucess'

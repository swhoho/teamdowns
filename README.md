# Project Title
Predicting House Prices in Seoul

# Table of Content

* [Contributors](#Contributors)
* [Synopsis](#Synopsis)
* [Prerequisites](#Prerequisites)
* [File Descriptions](#File_Descriptions)
* [Reference](#Reference)
* [External Link](#External_link)

# <a name="Contributors"></a>Contributors
* "Heemyung Kang" <gmlaud14@gmail.com>
* "Hojung Yeo" <swhoho@gmail.com>
* "Down Jung" <jdu2038@gmail.com>
* "Koo hala" <poiumn88@gmail.com>

# <a name="Synopsis"></a>Synopsis
The purpose of this project is to find the cost - efficient house for 20's and early 30's in South Korea who baerly afford to buy house with just one or two rooms. 
We try to predict the house price by using house options(aircondition, elevator....etc),distance data based on coordinate of the house and statistics data of each Dong(administrative district of Seoul equivalent to town).
We collected the house price and house information data in the site Dabang(https://www.dabangapp.com/).
You can quickly understand what the purpose of the project from https://prezi.com/o7xutcnjkbsf/predicting-house-prices-with-regression/

# <a name="Prerequisites"></a>Prerequisites

* Installing Selenium from https://christopher.su/2015/selenium-chromedriver-ubuntu/
* Setting up Mongo DB
* Python 2.7 or Python 3.3+
* Ipython Notebook 
* You don't need to install MongoDB and Selenium if you skip the data crawling part by using finalcsv.csv


# <a name="File_Descriptions"></a>File_Descriptions
* Crawling Datas.ipynb: ipython notebook describe the process to crawling datas
* visualization to modeling.ipynb: ipython notebook describe the preprocessing to modeling steps
* firstfile.py & secondfile.py: python code to execute data crawling process 
* image1.png,image2.png,image3.png,image4.png,besthouse.png, worsthouse.png: image file of dabang app 
* finalcsv.csv: csv file of the data structure to use for modeling
* bank.csv: csv file that show us the banks data of each dong in Seoul
* population.csv: csv file that show us the eldery population data of each dong in Seoul
* You can follow our project's process by executing Crawling Datas.ipynb -> visualization to modeling.ipynb orders


# <a name="Reference"></a>Reference
* Dabang[https://www.dabangapp.com/]
* Naver API from here [https://developers.naver.com/products/map]
* Mc Donalds Korea[www.mcdonalds.co.kr/]
* Starbucks korea[http://www.istarbucks.co.kr/index.do]
* Seoul Statistics[http://stat.seoul.go.kr/]


# <a name="External_link"></a>External Link
Prezi : https://prezi.com/o7xutcnjkbsf/predicting-house-prices-with-regression/

import requests
from fake_useragent import UserAgent
from lxml import etree
from pymysql import *
import pandas as pd
import pymysql
import os




if __name__=='__main__':
    url = 'http://bang.dangdang.com/books/'
    headers={
        'User-Agent':UserAgent().random
    }
    response=requests.get(url=url,headers=headers)
    page_text=response.text
    #print(page_text)

    tree=etree.HTML(page_text)
    div_list=tree.xpath('/html/body/div[2]/div')


    filepath=r'D:\Program Files (x86)\py_work\爬虫抓取后mysql存储\data'
    num=0
    for div in div_list:
        li_list=div.xpath('./div[2]/div/ul/li')
        for li in li_list:
            title=li.xpath('./p[2]/a/@title')[0]
            price=li.xpath('./p[1]/text()')[0]
            new_list=[[title,price]]
            name = ['title', 'price']
            test = pd.DataFrame(columns=name,data=new_list)
            num=num+1
            if num<=9:
                test.to_csv(filepath+'./book'+'0'+str(num)+'.csv')
            else:
                test.to_csv(filepath+'./book'+str(num)+'.csv')


    db=pymysql.connect(host='localhost',user='root',password='07kabuto',charset='utf8')
    cursor=db.cursor()

    sqlSentence1='create database if not exists bookDataBase'
    cursor.execute(sqlSentence1)
    sqlSentence2='use bookDataBase;'
    cursor.execute(sqlSentence2)

    fileList=os.listdir(filepath)
    for fileName in fileList:
        data=pd.read_csv(filepath+'/'+fileName,encoding='utf8')
        print('正在创建数据表%s'%fileName[0:6])
        sqlSentence3='create table if not exists %s '% fileName[0:6] +'(name VARCHAR(30),price float)'
        cursor.execute(sqlSentence3)
        print('正在存储%s'% fileName[0:6])
        length=len(data)
        for i in range(0,length):
            record=tuple(data.loc[i])
            print('record=',record)
            try:
                sqlSentence4="insert into %s"% fileName[0:6]+"(name,price) values (%s,%s);"%record
                #sqlSentence4=sqlSentence4.replace('nan','null').replace('None','null').replace('none','null')
                cursor.execute(sqlSentence4)
            except:
                break
    
    cursor.close()
    db.commit()
    db.close()

    db=pymysql.connect(host='localhost',user='root',password='07kabuto',charset='utf8')
    cursor=db.cursor()
    cursor.execute('use bookDataBase;')
    cursor.execute('select * from book01')
    results=cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    db.commit()
    db.close()




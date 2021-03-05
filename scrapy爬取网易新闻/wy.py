import scrapy
from selenium import webdriver
from wangyi_news.items import WangyiNewsItem
from os import devnull


class WySpider(scrapy.Spider):
    name = 'wy'
    #allowed_domains = ['https://news.163.com/']
    start_urls = ['https://news.163.com/']
    model_urls=[]

    def __init__(self):
        options=webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.bro=webdriver.Chrome(executable_path='./chromedriver.exe',options=options)
        #print('init运行成功！')

    def parse(self, response):
        li_list=response.xpath('//*[@id="js_festival_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        alist=[3,4,6,7,8]
        for index in alist:
            model_url=li_list[index].xpath('./a/@href').extract_first()
            self.model_urls.append(model_url)

        for url in self.model_urls:
            yield scrapy.Request(url,callback=self.parse_model)

    def parse_model(self,respose):
        div_list=respose.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title=div.xpath('./div/div[1]/h3/a/text()').extract_first()
            news_detail_url=div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item=WangyiNewsItem()
            item['title']=title
            if news_detail_url is None:
                continue
            yield scrapy.Request(url=news_detail_url,callback=self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        content=response.xpath('//*[@id="content"]/div[2]//text()').extract()
        content=''.join(content)
        item=response.meta['item']
        item['content']=content
        yield item


    def closed(self,spider):
        self.bro.quit()






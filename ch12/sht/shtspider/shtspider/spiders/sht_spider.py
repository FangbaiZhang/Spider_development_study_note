import scrapy
import re
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from shtspider.items import ShtspiderItem

class ShtSpider(scrapy.Spider):
    name = 'sht'
    allowed_domains = ['dsndsht23.com']
    start_urls = ['https://www.dsndsht23.com/forum-2-1.html']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        papers = soup.find_all('a', class_="s xst", href=re.compile(r'thread-.*'))
        for paper in papers:
            old_url = paper['href']
            # 解析出来的url和检查网页源代码看到的url有所变化，需要拼接上网站主域名
            # 可以用urljoin函数拼接，也直接可以用字符串相加拼接
            # full_url = 'https://www.dsndsht23.com/' + url
            page_url = 'https://www.dsndsht23.com/'
            url = urljoin(page_url, old_url)
            # full_url = 'https://www.dsndsht23.com/' + url
            title = paper.get_text()
            item = ShtspiderItem(url=url, title=title)
            request = scrapy.Request(url=url, meta={'item': item}, callback=self.parse_body)
            yield item


        '''
        next_page = soup.find('a', class_="nxt")
        next_page_url = 'https://www.dsndsht23.com/' + next_page['href']
        
        try:
            if next_page:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        except TypeError:
            print("爬取结束")
        '''

    def parse_body(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        image_url = soup.find('a', class_="s xst", href=re.compile(r'thread-.*'))




if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('sht')
    process.start()


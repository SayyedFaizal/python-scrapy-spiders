import scrapy
import re
from lxml import html
#from locations.items import GeojsonPointItem

class EarlsCa(scrapy.Spider):
    name = 'earls_ca_ws'
    brand_name = 'Earls' 
    spider_type = 'chain'
    chain_id = "3436"
    allowed_domains = ["earls.ca"]
    #start_url = ["https://earls.ca/"]
    url = "https://earls.ca/locations/"

    def start_requests(self):
        headers = {
            'authority': 'earls.ca',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://earls.ca/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }
        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response):
        html_content = response.body
        root = html.fromstring(html_content)
        allLocations = root.xpath("/html/head/script[4]/text()")
        id_r = re.findall('id: (.*?),',allLocations[0])
        name = re.findall('name: (.*?),',allLocations[0])
        lat = re.findall('lat: (.*?),',allLocations[0])
        lon = re.findall('long: (.*?),',allLocations[0])
        add = re.findall('address1: (.*?),',allLocations[0])
        city = re.findall('address2: (.*?),',allLocations[0])
        phone = re.findall('phone: (.*?),',allLocations[0])

        
        
        data = list(zip(id_r,lat,lon,name,add,city,phone))
        
        for res in data:
            finalData = {}
            finalData["ref"] = res[0]
            finalData["lat"] = res[1]
            finalData["lon"] = res[2]
            finalData["name"] = res[3]
            finalData["addr_full"] = res[4]
            finalData["city"] = res[5]
            finalData["country"] = "canada"
            finalData["phone"] = res[6]
            finalData["website"] = "https://www.earls.ca/"
            yield (finalData)



        

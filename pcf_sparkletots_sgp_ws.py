import scrapy
import json
import re
from lxml import html

#from locations.items import GeojsonPointItem



class PcfSparkletots_sgp(scrapy.Spider):
    name = "pcf_sparkletots_sgp_ws"
    brand_name = "PCF"
    spider_type = "chain"
    chain_id = "33710"
    allowed_domains = ["pcf.org.sg"]
    
    # start_urls = ["https://www.pcf.org.sg/sparkletots/"]
    url = "https://www.pcf.org.sg/sparkletots/our-preschools/"

    def start_requests(self):
        headers = {
            'authority': 'www.pcf.org.sg',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }
        yield scrapy.Request(
            url = self.url, 
            callback = self.parse,
            headers = headers
            )

    def parse(self, response):
        print("Response : {}".format(type(response)))
        root = html.fromstring(response.text)
        data = root.xpath("/html/body/script[18]/text()")
        raw = json.loads(data[0][18865:-111])
        for school in raw["objects"]:
            finalData = {}
            if isinstance(school["location"], dict):
                finalData["ref"] = school["id"]
                finalData["lat"] = school["location"]["lat"]
                finalData["lon"] = school["location"]["lng"]
                finalData["name"] = school["title"]
                add = re.findall('</strong><br>\s*(.*?)<br>',school["description"])
                ph = re.findall('Tel: (.*?)<br>',school["description"])
                em = re.findall('>(.*?)</a>',school["description"])
                finalData["addr_full"] = "".join(add)
                finalData["city"] = "singapore"
                finalData["postcode"] = school["postal_code"]
                finalData["country"] = "singapore"
                finalData["phone"] = "".join(ph)
                finalData["email"] = "".join(em)
                finalData["website"] = "https://www.pcf.org.sg/sparkletots/"
                yield(finalData)
        
import scrapy
import json
from lxml import html
import re
#from locations.items import GeojsonPointItem

class JugoJuiceCa(scrapy.Spider):
    name = "jugo_juice_ca_ws"
    brand = "Jugo Juice"
    spider_type = "chain"
    chain_id = "32945"
    allowed_domains = ["jugojuice.com"]
    #start_urls = ["https://jugojuice.com/"]

    url = "https://jugojuice.com/find-a-location/"

    def start_requests(self):
        headers = {
            'authority': 'jugojuice.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.bing.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }
        yield scrapy.Request (
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response,):
        root = html.fromstring(response.body)
        data_div = root.xpath('//*[@id="page-content"]/div/main/div/div/div/@data-map-markers')
        data_json = json.loads(data_div[0])

        for data in data_json:
            finalData = {}
            finalData["ref"] = data["id"]
            finalData["lat"] = data["position"]["lat"]
            finalData["lon"] = data["position"]["lng"]
            add_text = data["text"]
            add_root = html.fromstring(add_text)
            finalData["name"] = add_root.xpath('./p[1]/text()')[0]
            finalData["add_full"] = add_root.xpath('./p[2]/text()')[0]
            postcode_re = re.compile(r'\s\w\d\w\s\d\w\d')
            finalData["postcode"] = " ".join(postcode_re.findall(add_root.xpath('./p[2]/text()')[0])).strip()
            finalData["country"] = "Canada"
            finalData["website"] = "https://jugojuice.com/"

            yield(finalData)
            
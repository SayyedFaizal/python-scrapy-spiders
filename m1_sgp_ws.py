import scrapy
import json
import re
#from locations.items import GeojsonPointItem

class M1Sgp(scrapy.Spider):
    name = 'm1_sgp_ws'
    brand_name = 'M1' 
    spider_type = 'chain'
    chain_id = '26316'
    allowed_domains = ["m1.com.sg/"]
    
    # start_urls = ["https://www.m1.com.sg/"]

    url = "https://www.m1.com.sg/m1api/Map/ContactUs"

    def start_requests(self):
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
            'Referer': 'https://www.m1.com.sg/support/contact-us',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
            'accept': 'application/json',
            'x-dtpc': '3$75318868_206h4vHQGNSRUUFUFDFDRHUUCRGWCKEAKUFPHK-0e0',
        }
        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response):
        root = json.loads(eval(response.text))
        for index, store in enumerate(root["Stores"][0]["StoreTypes"][0]["StoresList"]):
            finalData = {}
            finalData["ref"] = index+1
            finalData["lat"] = store["Latitude"]
            finalData["lon"] = store["Longitude"]
            finalData["name"] = store["StoreTitle"]
            br_re = re.compile('^(.*?)<br')
            ad = br_re.findall(store["Description"])
            add = "".join(ad)
            if "span" in add :
                add = re.findall('">(.*?)</s',add)
                add = "".join(add)
            pho = re.findall('\d\d\d\d\d\d\<',store["Description"])
            post = "".join(pho)[:-1]
            finalData["addr_full"] = add
            finalData["postcode"] = post
            finalData["country"] = "singapore"
            finalData["website"] = "https://www.m1.com.sg/"

            yield(finalData)

            
            

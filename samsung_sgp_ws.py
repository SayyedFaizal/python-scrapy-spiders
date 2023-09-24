import scrapy
import json
from lxml import html
#from locations.items import GeojsonPointItem

class SamsungSgp(scrapy.Spider):
    name = 'samsung_sgp_ws'
    brand_name = 'Samsung' 
    spider_type = 'chain'
    chain_id = "7671"
    allowed_domains = ["samsung.com/sg"]

    #start_url = ["https://www.samsung.com/sg/"]

    url = "https://www.samsung.com/sg/samsung-experience-store/locations/"

    def start_requests(self):
        headers = {
            'authority': 'www.samsung.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-modified-since': 'Tue, 29 Aug 2023 02:44:17 GMT',
            'if-none-match': '"48bc3-60406c988fd68"',
            'referer': 'https://www.samsung.com/sg/samsung-experience-store/about/',
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
        allLocations = root.xpath('//*[@id="content"]/div/div/div[1]/div/div[2]/script[3]/text()')
        datac = allLocations[0]
        datac.strip()
        datajson = datac[25:8042]
        pureData = datajson.replace('.jpg",','"')
        
            
        stores = json.loads(pureData)
        

        for store in stores: 
            finalData = {}
            finalData["ref"] = store["storeId"]
            finalData["lat"] = store["lattitude"]
            finalData["lon"] = store["longitude"]
            finalData["name"] = store["storeName"]
            finalData["add_full"] = store["addressLine1"]
            finalData["state"] = store["state"]
            finalData["country"] = store["suburb"]
            finalData["opening_nours"] = {}

            c = store["daily"].split("to")
            tm = []
            for i in c:
                time2 = i.replace("am", "").replace("pm", "").strip()
                if ":" not in time2:
                    time2 += ":00"
                if "am" in i:
                    time2 = int(time2[:-3])
                    if time2 < 10:
                        time2 = "0"+str(time2)+":00"
                    else:
                        time2 = str(time2)+":00"
                if "pm" in i:
                    time2 = str(int(time2[:-3]) + 12) + ":00"
                tm.append(time2)
            hrs = "Mo-Su "+"-".join(tm)
            finalData["opening_nours"]["stores"] = [hrs]
            finalData["website"] = "https://www.samsung.com/sg"

            yield(finalData)


        
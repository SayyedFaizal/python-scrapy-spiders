import scrapy
import json
#from locations.items import GeojsonPointItem

class MarieClaireCa(scrapy.Spider):
    name = 'marie_claire_ca_ws'
    brand_name = 'Marie Claire' 
    spider_type = 'chain'
    chain_id = "32968"
    allowed_domains = ["marie-claire.com"]

    # start_url = ["https://www.marie-claire.com/"]
    url = "https://stockist.co/api/v1/u8717/locations/all"

    def start_requests(self):

        headers = {
            'authority': 'www.marie-claire.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'if-none-match': 'W/"cacheable:73385e29402dca5955762140c344f617"',
            'referer': 'https://www.bing.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }

        yield scrapy.Request (
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response):
        stores = json.loads(response.body)
        
        for store in stores:
            finalData = {}
            finalData["ref"] = store["id"]
            finalData["lat"] = store["latitude"]
            finalData["lon"] = store["longitude"]
            finalData["name"] = store["name"]
            finalData["addr_full"] = store["address_line_1"]
            finalData["city"] = store["city"]
            finalData["state"] = store["state"]
            finalData["postcode"] = store["postal_code"]
            finalData["country"] = store["country"]
            finalData["phone"] = store["phone"]
            hrs_data = store["custom_fields"]
            opening_hrs = {}
            for i in hrs_data:
                day = i["name"]
                hr = i["value"].replace("h",":")
                day = day[4:-1]
                opening_hrs[day] = hr
            finalData["opening_hours"] = opening_hrs
            finalData["website"] = "https://www.marie-claire.com/"
            
            yield(finalData)
            
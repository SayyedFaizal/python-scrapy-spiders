import scrapy
import json
#from locations.items import GeojsonPointItem

class BentleyCa(scrapy.Spider):
    name = 'bentley_ca_ws'
    brand_name = 'Bentley' 
    spider_type = 'chain'
    chain_id = '301'
    allowed_domains = ["bentleymotors.com"]

    url = "https://www.bentleymotors.com/content/brandmaster/global/bentleymotors/en/apps/dealer-locator/jcr:content.api.750601ee688bbd0f15bc706e1fccfa45.json"

    url_to_parse = ''

    def start_requests(self):
        headers = {
            'authority': 'www.bentleymotors.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }

        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers,
        )
    
    def parse(self, response):
        data = json.loads(response.body)
        dealers = data["dealers"]
        for dealer in dealers:
            if dealer["countryId"]=="CA":
                self.url_to_parse = "https:"+dealer["url"] 
                yield scrapy.Request(self.url_to_parse,callback=self.parse_url)
        
    
    def parse_url(self,response):
        data1 = json.loads(response.body)
        add = data1["addresses"][0]
        finalData ={}
        finalData["ref"] = data1["id"]
        finalData["lat"] = add["wgs84"]["lat"]
        finalData["lon"] = add["wgs84"]["lng"]
        finalData["name"] = data1["dealerName"]
        finalData["addr_full"] = add["street"]+" "+add["city"]+" "+add["postcode"]
        finalData["street"] = add["street"]
        finalData["ciity"] = add ["city"]
        finalData["state"] = add["county"]
        finalData["postcode"] = add["postcode"]
        finalData["country"] = add["country"]
        finalData["phone"] = add["departments"][0]["phone"]
        if add["postcode"] == "T2H 2V4":
            finalData["website"] = ""
            finalData["email"] = ""
        else:
            finalData["website"] = add["departments"][0]["website"]
            finalData["email"] = add["departments"][0]["email"]
        yield(finalData)
    

         
            
         
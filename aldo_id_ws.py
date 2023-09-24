import scrapy
import re
import json
#from locations.items import GeojsonPointItem

class aldo_id(scrapy.Spider):
    name = 'aldo_id_ws'
    brand_name = 'Aldo' 
    spider_type = 'chain'
    allowed_domains = ["aldoshoes.co.id/"]
    
    # start_urls = ["https://www.m1.com.sg/"]

    url = "https://www.aldoshoes.co.id/storelocator/index/loadstore/"
    def start_requests(self):
        yield scrapy.Request(
                url = self.url,
                callback = self.parse,
                
            )
    def parse(self, response):
        # Using File as Storing response
        print("Response : {}".format(type(response)))
        stores = json.loads(response.body)
        

        for store in stores["storesjson"]:
            finalData = {}
            finalData["ref"] = store["storepickup_id"]
            finalData["lat"] = store["latitude"]
            finalData["lon"] = store["longitude"]
            finalData["name"] = store["store_name"]
            finalData["add_full"] = store["address"] 
            finalData["phone"] = store["phone"]
            finalData["website"] = "https://www.aldoshoes.co.id/"

            yield(finalData)


            #import pdb
            #pdb.set_trace()
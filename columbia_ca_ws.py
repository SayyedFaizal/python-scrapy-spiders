import scrapy
import json
#from locations.items import GeojsonPointItem


class ColumbiaCa(scrapy.Spider):
    name = "columbia_ca_ws"
    brand = "columbia"
    spider_type = "chain"
    chain_id = "20801"

    allowed_domains = ["columbia.com"]
    #start_url = ["https://columbia.com"]

    url = "https://columbia.locally.com/stores/conversion_data?has_data=true&company_id=67&store_mode=&style=&color=&upc=&category=&inline=1&show_links_in_list=&parent_domain=&map_ne_lat=55.96055609477247&map_ne_lng=-55.227315227229596&map_sw_lat=31.183165028205195&map_sw_lng=-99.04079178973001&map_center_lat=43.57186056148883&map_center_lng=-77.13405350847981&map_distance_diag=2835.374929769489&sort_by=proximity&no_variants=0&only_retailer_id=&dealers_company_id=67&only_store_id=false&uses_alt_coords=false&q=false&zoom_level=4&lang=en-us&currency=USD"

    def start_requests(self):
        headers = {
            'authority': 'columbia.locally.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://columbia.locally.com/conversion?company_name=Columbia&company_id=67&inline=1&category=&lang=en-us&currency=USD&dealers_company_id=67&host_domain=www.columbia.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'x-requested-with': 'XMLHttpRequest',
        }
        
        yield scrapy.Request(
            url= self.url,
            headers= headers
        )

    def parse(self, response):
        data = json.loads(response.body)
        for store in data["markers"]:
            if store["country"] == "CA":
                finalData = {}
                finalData["ref"] = store["id"]
                finalData["lat"] = store["lat"]
                finalData["lon"] = store["lng"]
                finalData["name"] = store["name"]
                finalData["addr_full"] = store["address"]
                finalData["city"] = store["city"]
                finalData["state"] = store["state"]
                finalData["postcode"] = store["zip"]
                finalData["country"] = "canada"
                finalData["phone"] = store["phone"]
                finalData["website"] = "https://www.columbia.com/"
                
                yield(finalData)
        

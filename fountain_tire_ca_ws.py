import scrapy
import json
import csv
#from locations.items import GeojsonPointItem

class FountainTireCa(scrapy.Spider):
    name = "fountain_tire_ca_ws"
    brand = "Fountain Tire"
    spidet_type = "chain"
    chain_id = "4534"

    allowed_domains = ["fountaintire.com"]
    #start_url = ["https://www.fountaintire.com"]
    url = "https://www.fountaintire.com/umbraco/api/locations/get"
    id_list = []
    def start_requests(self):
        headers = {
            'authority': 'www.fountaintire.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.fountaintire.com',
            'referer': 'https://www.fountaintire.com/contact-us/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }
        row_count = 0
        payload = {}
        with open('data/canada_world_cities.csv') as location_file:
            location_reader = csv.DictReader(location_file)

            for row in location_reader:
                row_count = row_count + 1
                payload["latitude"] = row["latitude"]
                payload["longitude"] = row["longitude"]
                payload["radius"] = "300"
                payload["services"] = []

                yield scrapy.Request(
                    url = self.url,
                    callback = self.parse,
                    method= "POST",
                    body= json.dumps(payload),
                    headers = headers,
                )
    
    def parse(self, response):
        data = json.loads(response.body)
        for store in data:
            if store["id"] not in self.id_list:
                self.id_list.append(store["id"])
                finalData = {}
                finalData["ref"] = store["id"]
                finalData["lat"] = store["lat"]
                finalData["lon"] = store["lng"]
                finalData["name"] = store["title"]
                finalData["addr_full"] = store["fullAddress"]
                finalData["city"] = store["city"]
                finalData["state"] = store["province"]
                finalData["postcode"] = store["postalCode"]
                finalData["country"] = "canada"
                finalData["phone"] = store["phoneNumber"]
                finalData["email"] = store["email"]


                yield(finalData)
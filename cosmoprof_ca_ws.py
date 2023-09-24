import scrapy
import json
import csv
from lxml import html
#from locations.items import GeojsonPointItem


class CosmoProfCa(scrapy.Spider):
    name = "cosmoprof_ca_ws"
    brand = "Cosmo Prof"
    spider_type = "chain"
    chain_id = "200003436"

    allowed_domians = ["cosmoprofbeauty.com"]
    #start_url = ["https://www.cosmoprofbeauty.com"]
    url = "https://maps.cosmoprofbeauty.com/api/getAsyncLocations?template=search&level=search&search={},%20Canada"
    id_list = []
    def start_requests(self):
        headers = {
            'authority': 'stores.cosmoprofbeauty.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.cosmoprofbeauty.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }

        row_count = 0
        with open('data/canada_world_cities.csv') as location_file:
            location_reader = csv.DictReader(location_file)

            for row in location_reader:
                row_count = row_count + 1
                n_url = self.url.format(row['city'])

                yield scrapy.Request(
                    url = n_url,
                    callback = self.parse,
                    headers = headers,
                )
    def parse(self, response):
        data = json.loads(response.text)
        if data["maplist"] != "" :
            for store in data["markers"]:
                finaldata = {}
                add = html.fromstring(store["info"])
                add_data = json.loads(add.xpath("./text()")[0])
                if add_data["fid"] not in self.id_list:
                    finaldata["ref"] = add_data["fid"]
                    finaldata["lat"] = add_data["lat"]
                    finaldata["lon"] = add_data["lng"]
                    finaldata["name"] = add_data["location_name"]
                    finaldata["addr_full"] = add_data["address_1"]+add_data["address_2"]
                    finaldata["city"] = add_data["city"]
                    finaldata["state"] = add_data["region"]
                    finaldata["postcode"] = add_data["post_code"]
                    finaldata["country"] = "canada"
                    self.id_list.append(add_data["fid"])

                    yield(finaldata)
    



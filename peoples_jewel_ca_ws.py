import scrapy
import json 
import csv
#from locations.items import GeojsonPointItem

class PeoplesJewelCa(scrapy.Spider):
    name = "peoples_jewel_ca_ws"
    brand = "Peoples Jewellers"
    spider_type = "chain"
    chain_id = "200002224"
    allowed_domains = ["peoplesjewellers.com"]

    #start_urls = ["https://www.peoplesjewellers.com/"]
    url = 'https://stores.peoplesjewellers.com/umbraco/api/search/GetDataByCoordinates?longitude={}&latitude={}&distance=25&units=kilometers&filter='
    list_id = []
    def start_requests(self):
        headers = {
            'authority': 'stores.peoplesjewellers.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://stores.peoplesjewellers.com/results?q=Vancouver,%20BC,%20Canada',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'x-requested-with': 'XMLHttpRequest',
        }
        row_count = 0
        with open('data/canada_world_cities.csv') as location_file:
            location_reader = csv.DictReader(location_file)

            for row in location_reader:
                row_count = row_count + 1
                n_url = self.url.format(row['longitude'], row['latitude'])

                yield scrapy.Request(
                    url = n_url,
                    headers = headers,
                )
    
    def parse(self, response):
        
        data = eval(response.text)
        stores = json.loads(data)
        if stores["TotalResults"] != "0":
            for store in stores["StoreLocations"] :
                if store["ExtraData"]["ReferenceCode"] not in self.list_id:
                    finalData = {}
                    finalData["ref"] = store["ExtraData"]["ReferenceCode"]
                    self.list_id.append(store["ExtraData"]["ReferenceCode"])
                    finalData["lat"] = store["Location"]["coordinates"][1]
                    finalData["lon"] = store["Location"]["coordinates"][0]
                    finalData["name"] = store["Name"]
                    finalData["add_full"] = store["Address"]
                    finalData["housenumber"] = store["ExtraData"]["Address"]["AddressNonStruct_Line2"]
                    finalData["city"] = store["ExtraData"]["Address"]["Locality"]
                    finalData["state"] = store["ExtraData"]["Address"]["RegionName"]
                    finalData["postcode"] = store["ExtraData"]["Address"]["PostalCode"]
                    finalData["country"] = "canada"
                    finalData["phone"] = store["ExtraData"]["Phone"]

                     
                    yield(finalData)
               
                


                

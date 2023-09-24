import scrapy
import json
#from locations.items import GeojsonPointItem

class RwAndCoCA(scrapy.Spider):
    name = "rw-co_ca_ws"
    brand = "Rw&Co"
    spider_type = "chain"
    chain_id = "30932"
    allowed_domains = ["rw-co.com"]
    #start_url = [""https://www.rw-co.com/""]
    url = "https://sls-api-service.sweetiq-sls-production-east.sweetiq.com/6prxb7CIG6VQbQTIwIIgdEhpd9FoYK/locations-details?locale=en_CA&ids=2617905%2C3561345%2C2617941%2C2617947%2C2617904%2C2617917%2C2617901%2C2617889%2C2617916%2C2617938%2C2617880%2C2617900%2C2617952%2C2617877%2C2617879%2C2617932%2C2617934%2C2617920%2C2617948%2C2617876%2C2617931%2C2617942%2C2617945%2C2617914%2C2617924%2C3075415%2C3075171%2C2617943%2C2617939%2C2617933%2C2617883%2C2617902%2C2617950%2C2617894%2C2617891%2C2617878%2C3561360%2C2617944%2C2617893%2C2617899%2C2617881%2C2617929%2C2617915%2C2617935%2C2617906%2C2617937%2C2617890%2C2617953%2C2617887%2C4057989%2C2617885%2C2617926%2C2617911%2C2617928%2C2617897%2C2617907%2C2617940%2C2617919%2C2617936%2C2617923%2C2617898%2C2617903%2C2617927%2C2617954%2C2617912%2C2617892%2C2617886%2C2617908%2C2617951%2C2617946%2C2617895%2C2617922%2C3540157%2C2617896%2C2617875%2C2617921%2C2617909%2C2617910%2C2617918%2C2617925%2C2617884%2C2617930&clientId=5fc54810ae5334a2323b2dea&cname=locations.rw-co.com"

    def start_requests(self):
        headers = {
            'authority': 'sls-api-service.sweetiq-sls-production-east.sweetiq.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://locations.rw-co.com',
            'referer': 'https://locations.rw-co.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'x-api-key': '',
        }
        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response):
        data = json.loads(response.body)
        for store in data["features"]:
            finalData = {}
            finalData["ref"] = store["properties"]["id"]
            finalData["lat"] = store["geometry"]["coordinates"][1]
            finalData["lon"] = store["geometry"]["coordinates"][0]
            finalData["name"] = store["properties"]["name"]
            finalData["addr_full"] = store["properties"]["addressLine1"]
            finalData["city"] = store["properties"]["city"]
            finalData["state"] = store["properties"]["province"]
            finalData["postcode"] = store["properties"]["postalCode"]
            finalData["country"] = "canada"
            finalData["phone"] = store["properties"]["phoneNumber"]
            finalData["opening_hours"] = store["properties"]["hoursOfOperation"]
            finalData["website"] = "https://www.rw-co.com/"
            yield(finalData)
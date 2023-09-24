import scrapy
import json
from lxml import html
#from locations.items import GeojsonPointItem

class MaxPl(scrapy.Spider):
    name = "max_pl_ws"
    brand = "Max"
    spider_type = "chain"
    chain_id = "2599"

    allowed_domains = ["maxpremiumburgers.pl"]

    #start_url = ["https://www.maxpremiumburgers.pl/"]
    url = "https://www.maxpremiumburgers.pl/znajdz-max/restauracje/"

    def start_requests(self):
        headers = {
            'authority': 'www.maxpremiumburgers.pl',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.maxpremiumburgers.pl/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }
        yield scrapy.Request(
            url= self.url,
            callback= self.parse,
            headers= headers
        )
    def parse(self, response, **kwargs):
        root = html.fromstring(response.text)
        data = json.loads(root.xpath("/html/body/div[1]/main/div[1]/@data-props")[0])
        for index, store in enumerate(data["restaurants"]):
            finalData = {}
            finalData["ref"] = index+1
            finalData["lat"] = store["latitude"]
            finalData["lon"] = store["longitude"]
            finalData["name"] = store["name"]
            finalData["addr_full"] = store["streetAddress"]+" "+store["city"]
            finalData["city"] = store["city"]
            finalData["postcode"] = store["postalCode"]
            finalData["country"] = "poland"
            finalData["website"] = "https://www.maxpremiumburgers.pl"
            yield(finalData)

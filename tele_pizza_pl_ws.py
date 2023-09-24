import scrapy
from lxml import html
#from locations.items import GeojsonPointItem

class TelePizzaPl(scrapy.Spider):
    name = "tele_pizza_pl_ws"
    brand = "t-pizza"
    spider_type = "chain"
    chain_id = "1969"

    allowed_domians = ["tpizza.pl"]
    #start_url = ["https://www.tpizza.pl/lokale/"]
    url = "https://www.tpizza.pl/lokale/"

    def start_requests(self):
        headers = {
            'authority': 'www.tpizza.pl',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.tpizza.pl/',
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
        data = root.xpath('//*[@class="elementor-accordion-item"]')
        count = 0
        for store in data:
            finalData = {}
            nam = store.xpath('./div/p/a/strong/text()')
            addr_ = store.xpath('./div/p/strong/text()')
            ph = store.xpath('./div/p[2]/text()')

            for i,j in zip(nam,addr_):
                count +=1
                finalData["ref"] = count
                finalData["name"] = i
                finalData["addr_full"] = j
                finalData["country"] = "poland"
                finalData["phone"] = "" if len(ph) > 1 else "".join(ph)
                finalData["website"] = "https://www.tpizza.pl/"
                finalData["opening_hours"] = ["Mo-Th 11:00-23:00","Fr-Sa 11:00-24:00"]
                yield(finalData)
        

            

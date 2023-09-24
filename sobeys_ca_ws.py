import scrapy
from lxml import html
#from locations.items import GeojsonPointItem

class SobeysCa(scrapy.Spider):
    name = 'sobeys_ca_ws'
    brand_name = 'Sobeys' 
    spider_type = 'chain'
    chain_id = '1434'
    allowed_domains = ["sobeys.com"]

    # start_urls = ["https://www.sobeys.com/en/"]
    url = "https://www.sobeys.com/store-locator/"

    def start_requests(self):
        headers = {
            'authority': 'www.sobeys.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'referer': 'https://www.sobeys.com/en/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }

        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response,):
        root = html.fromstring(response.body)
        data_path = root.xpath('//*[@id="list-stores-wrap"]')
        for data in data_path:
            finalData = {}
            ref = data.xpath('./div/@data-id')
            lat = data.xpath('./div/@data-lat')
            lon = data.xpath('./div/@data-lng')
            city = data.xpath('./div/@data-city')
            state = data.xpath('./div/@data-province')
            postcode = data.xpath('./div/@data-postal-code')
    
            for i in range(0,len(ref)):
                finalData["ref"] = ref[i]
                finalData["lat"] = lat[i]
                finalData["lon"] = lon[i]
                finalData["name"] = data.xpath(f'./div[@data-id = "{ref[i]}"]/div/div/h4/a/span/text()')[0]
                addr_full = data.xpath(f'./div[@data-id = "{ref[i]}"]/div/div/p/span/text()')
                add = " ".join(addr_full)
                finalData["addr_full"] = add
                finalData["city"] = city[i]
                finalData["state"] = state[i]
                finalData["postcode"] = postcode[i]
                finalData["country"] = "canada"
                finalData["phone"] = data.xpath(f'./div[@data-id = "{ref[i]}"]/div/div/span/a/text()')[0]
                finalData["website"] = 'https://www.sobeys.com/en/'
                
                
                yield(finalData)

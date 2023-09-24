import scrapy
from lxml import html
#from locations.items import GeojsonPointItem

class HotAndRollMay(scrapy.Spider):
    name = 'hotandroll_may_ws'
    brand_name = 'Hotandroll' 
    spider_type = 'chain'
    chain_id = '21743'
    allowed_domains = ["hotandroll.com/my"]
    
    # start_urls = ["https://hotandroll.com/"]

    url = "https://hotandroll.com/my/store-locator-7/"
    def start_requests(self):
        headers = {
            'authority': 'hotandroll.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
        }

        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )
    
    def parse(self, response):
        root = html.fromstring(response.body)
        data_path = root.xpath('//div[@class ="card h-100"]')

        for ref,data in enumerate(data_path):
            finalData = {}
            finalData["ref"] = str(ref+1)
            finalData["name"] = data.xpath('./div/h5/text()')[0]
            finalData["addr_full"] = data.xpath('./div/p/text()')[0]
            finalData["opening_hours"] = {}
            hrs = data.xpath('./div/p/following-sibling::p/text()')[0].split("-")
            timeList = []
            for i in hrs:
                time2 = i.replace("am", "").replace("pm", "").strip()
                if "pm" in i:
                    time2 = str(int(time2) + 12)
                time2 = time2+":00"
                timeList.append(time2)
            ftime = "Mo-Su "+"-".join(timeList)
            finalData["opening_hours"]["stores"] = [ftime]
            finalData["country"] = "Malaysia"
            finalData["website"] = "https://hotandroll.com/"
            yield(finalData)
            
        
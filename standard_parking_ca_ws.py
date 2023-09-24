import scrapy
import json
from lxml import html

class StandardParking(scrapy.Spider):
    name = "standard_parking_ca_ws"
    brand = "Standard Parking"
    spider_type = "chain"
    chain_id = "2542"

    allowed_domains = ["parking.com"]

    #start_url = [""]
    url = "https://parking.com/ca/cities"
    headers = {
        'Referer': 'https://parking.com/ca/cities',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        yield scrapy.Request(
            url= self.url,
            callback= self.parse,
            headers= self.headers
        )
    def parse(self, response,):
        root = html.fromstring(response.text)
        cities = root.xpath('//*[@id="app"]/div[3]/div/div[2]/div[2]/div[2]/div/ul/li/a/text()')
        for city in cities:
            city_url = "https://parking.com/{}/".format(city.lower())
            print(city_url)
            yield scrapy.Request(
                url= city_url,
                callback= self.city_parse,
                headers= self.headers
            )
    def city_parse(self, response):
        root = html.fromstring(response.text)
        data = root.xpath('/html/body/script[2]/text()')
        print(data[0].strip())
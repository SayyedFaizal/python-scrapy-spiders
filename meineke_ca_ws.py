import scrapy
import re
from lxml import html
#from locations.items import GeojsonPointItem

class MeinekeCa(scrapy.Spider):
    name = "meineke_ca_ws"
    brand = "Meineke"
    spider_type = "chain"
    chain_id = "1692"

    allowed_domains = ["meineke.ca"]

    #start_url = ["https://www.meineke.ca/"]
    url = "https://www.meineke.ca/locations/"
    states_url = ""
    city_url = ""
    state_list = []
    id_list = []
    
    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.meineke.ca/locations/on/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }
        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers,
        )

    def parse(self, response):
        index = html.fromstring(response.text)
        states_div = index.xpath('//*[@id="site-content"]/div[3]/div[2]/div/div/div[1]//a/@href')
        for a in states_div:
            self.states_url = "https://www.meineke.ca"+a
            self.state_list.append(a)
            
            yield scrapy.Request(self.states_url,callback=self.states_url_parse)
    
    def states_url_parse(self, response):
        index = html.fromstring(response.text)
        city_div = index.xpath('//*[@id="site-content"]/div[2]/div[2]/div[1]/div//a/@href')

        for a in city_div:
            for i in self.state_list:
                self.city_url ="https://www.meineke.ca"+i+a 
                
                yield scrapy.Request(self.city_url,callback=self.city_url_parse)

    def city_url_parse(self, response):
        index = html.fromstring(response.text)
        data = index.xpath('//*[@id="site-content"]/div[4]/div/div[2]/div/div/div/section[1]/div/div/@ng-click')
        for  store in data:
            store.strip()
            id_r = re.findall("(\d+)",store)
            coor_raw = re.findall('(\d+)\.(\d+)',store)
            add = re.findall('streetAddress1: (.*?),',store)
            state = re.findall('locationState: (.*?),',store)
            city = re.findall('locationCity: (.*?),',store)
            post = re.findall('locationPostalCode: (.*?),',store)
            phone = re.findall('phone: (.*?),',store)
            if id_r[4] not in self.id_list:
                self.id_list.append(id_r[4])
                finalData = {}
                finalData['ref'] = id_r[4]
                finalData['Lat'] = ".".join(coor_raw[0])
                finalData['Lon'] = "-"+".".join(coor_raw[1])
                finalData['name'] = "Meineke#"+id_r[4]
                finalData['addr_full'] = "".join(add).replace("'","")
                finalData['city'] = "".join(city).replace("'","")
                finalData['state'] = "".join(state).replace("'","")
                finalData['postcode'] = "".join(post).replace("'","")
                finalData['country'] = "canada"
                finalData['phone'] = "".join(phone).replace("'","")
                finalData['website'] = "https://www.meineke.ca/"
                yield (finalData)
            
            
        

        
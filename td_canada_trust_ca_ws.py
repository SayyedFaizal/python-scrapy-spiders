import scrapy
import json
#from locations.items import GeojsonPointItem

class TdCanadaTrustCa(scrapy.Spider):
    name = "td_canada_trust_ca_ws"
    allowed_domains = ["tdbank.com"]
    brand = "Td"
    spider_type = "chain"
    chain_id = "1376"

    #start_url = ["https://www.tdbank.com"]
    url = "https://www.tdbank.com/net/get12.ashx?longitude=-100.493984&latitude=49.1928819&country=CA&locationtypes=3&json=y&searchradius=50000&searchunit=km&numresults=10000"

    def start_requests(self):
        headers = {
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.td.com/',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        yield scrapy.Request(
            url = self.url,
            callback = self.parse,
            headers = headers
        )

    def parse(self, response):
        data = json.loads(response.body)
        branches = data["markers"]["marker"]
        for branch in branches:
            finalData = {}
            finalData["ref"] = branch["id"]
            finalData["lat"] = branch["lat"]
            finalData["lon"] = branch["lng"]
            finalData["name"] = branch["name"]
            finalData["addr_full"] = branch["address"]
            house = branch["address"].split(",")
            finalData["housenumber"] = house[0]
            finalData["city"] = house[-3]
            finalData["state"] = house[-2]
            finalData["postcode"] = house[-1]
            finalData["country"] = "canada"
            finalData["phone"] = branch["phoneNo"]
            if len(branch["hours"]) != 0: 
                week_day = ['Mo','Tu','We','Th','Fr','Sa','Su']

                final_hours = dict(zip(week_day, branch["hours"].values()))
                d=[]
                for w in week_day:
                    hrs = final_hours[w]
                    c = hrs.split("-")
                    for i in c:
                        time = i.replace("AM","").replace("PM","").strip()
                        if "AM" in i:
                            time = int(time[:-3])
                            if time < 10:
                                time = "0"+str(time)+":00"
                            else:
                                time = str(time)+":00"
                        if "PM" in i:
                            time = str(int(time[:-3]) + 12) + ":00"
                        d.append(time)
                    final_hours[w] = "-".join(d)
                    d=[]
                finalData["opening_hours"] = final_hours
            else:
                finalData["opening_hours"] = branch["hours"]
            finalData["website"] = "https://www.td.com/"
            yield(finalData)
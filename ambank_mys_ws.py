import scrapy
from lxml import html

class AmbankMys(scrapy.Spider):
    name = "ambank_mys_ws"
    brand = "Ambank"
    spider_type = "chain"
    chain_id = "7085"

    allowed_domains =["ambankgroup.com"]

    url = "https://www.ambankgroup.com/eng/locator/Pages/ATM.aspx"

    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'BIGipServercorporate_website_443_pool=!ePDCVMCfXUXjCSwkfWD5a2PbXYr1bnNBNsNl4fYMdIhBCmv2xLLmpotMO4NUNrtUyACwfGIhrAVMGSGuOvmb0Kuq9Eyv+DZZJKD3u/Tw; TS01040e85=01117c6e194932f62a6962a3cb008e89667487c7369d4cb50afc9bc69fb5ff634f64eee1be8a157a255bc46619119c887c477828703ee4490cbc168303034b98ca7200ef1d; _gid=GA1.2.1063038472.1694071927; _dc_gtm_UA-40131098-3=1; _ga=GA1.1.129096627.1694071927; TS0510666b027=0836ebe99dab200055baeb38508dc50c953ad7831cf6e8b23a635a56c9fb64196ca9bfefd12ed1970884371bf6113000e41bd1345adfb2be59ff3f8ba1ca8b0f55c755fbf05358b7411a43731e619e81a6bc0b636eb94b5dfe724eb292b82f70; _ga_MC6V4LNJ5L=GS1.1.1694071927.1.0.1694071938.49.0.0',
            'Origin': 'https://www.ambankgroup.com',
            'Referer': 'https://www.ambankgroup.com/eng/locator/Pages/ATM.aspx',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        yield scrapy.Request(
            url= self.url,
            callback= self.parse,
            headers= headers
        )

    def parse(self, response, **kwargs):
        root = html.fromstring(response.text)
        states = root.xpath('//*[@id="ctl00_m_g_5e0d93fc_c7bc_4948_9f41_01158c8ffb5e_ddlState"]/option/text()')
        del states[0]
        for state in states:
            data = {
                'MSOWebPartPage_PostbackSource': '',
                'MSOTlPn_SelectedWpId': '',
                'MSOTlPn_View': '0',
                'MSOTlPn_ShowSettings': 'False',
                'MSOGallery_SelectedLibrary': '',
                'MSOGallery_FilterString': '',
                'MSOTlPn_Button': 'none',
                '__EVENTTARGET': 'ctl00$m$g_5e0d93fc_c7bc_4948_9f41_01158c8ffb5e$LinkButton1',
                '__EVENTARGUMENT': '',
                '__REQUESTDIGEST': '0xBFF0D6F44F9A4380D29212FB5A2891BD1149D354157EA5571A2DFCC5D163730A0B99FFDB5D16211D097D2E792940461BBBF2BB38C22A8189D70B2EF0DBEA652B,07 Sep 2023 07:31:46 -0000',
                'MSOSPWebPartManager_DisplayModeName': 'Browse',
                'MSOSPWebPartManager_ExitingDesignMode': 'false',
                'MSOWebPartPage_Shared': '',
                'MSOLayout_LayoutChanges': '',
                'MSOLayout_InDesignMode': '',
                '_wpSelected': '',
                '_wzSelected': '',
                'MSOSPWebPartManager_OldDisplayModeName': 'Browse',
                'MSOSPWebPartManager_StartWebPartEditingName': 'false',
                'MSOSPWebPartManager_EndWebPartEditing': 'false',
                '__VIEWSTATE': '/wEPDwUBMA9kFgJmD2QWAgIBD2QWBAIBD2QWAgIJD2QWAmYPZBYCZg8WAh4TUHJldmlvdXNDb250cm9sTW9kZQspiAFNaWNyb3NvZnQuU2hhcmVQb2ludC5XZWJDb250cm9scy5TUENvbnRyb2xNb2RlLCBNaWNyb3NvZnQuU2hhcmVQb2ludCwgVmVyc2lvbj0xNC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj03MWU5YmNlMTExZTk0MjljAWQCAw9kFgYCBA9kFggFJmdfNGJlY2I4MDhfMGJiMl80YTU2XzhlOWNfNTU4ZGQ4ZWRhOTBlD2QWAmYPZBYCZg8PFgIeBFRleHQF5QI8dGFibGUgd2lkdGg9JzEwMCUnIGJvcmRlcj0nMCcgY2VsbHBhZGRpbmc9JzAnIGNlbGxzcGFjaW5nPScwJyBhbGlnbj0nbGVmdCc+PHRyPjx0ZCBjbGFzcz0nc3ViTGlua190ZXh0Jz48YSBocmVmPSdodHRwczovL3d3dy5hbWJhbmtncm91cC5jb20vZW5nJyBjbGFzcz0nZnhTdWJMaW5rX3RleHQnPkhvbWU8L2E+ID4gPGEgaHJlZj0naHR0cHM6Ly93d3cuYW1iYW5rZ3JvdXAuY29tL2VuZy9Mb2NhdG9yJyBjbGFzcz0nZnhTdWJMaW5rX3RleHQnPkxvY2F0ZSBVczwvYT4gPiA8YSBocmVmPScvZW5nL2xvY2F0b3IvUGFnZXMvQVRNLmFzcHgnIGNsYXNzPSdmeFN1YkxpbmtfdGV4dCc+QVRNczwvYT48L3RkPjwvdHI+PC90YWJsZT5kZAUmZ19jNzUzYzZkZl83MGFkXzQwYmRfODQwNl83MjA5Y2Q3NDliNTIPZBYEZg8WAh4HVmlzaWJsZWhkAgEPFgIfAmhkBSZnX2VkNmVhMDVmX2MwNDBfNDc1Yl9iMWI2Xzg5NWI5ZTc3NmNlNg9kFgRmDxYCHwJoZAIBDxYCHwJoZAUmZ181ZTBkOTNmY19jN2JjXzQ5NDhfOWY0MV8wMTE1OGM4ZmZiNWUPZBYMAgEPDxYCHwEFEEZpbmQgQW1CYW5rIEFUTXNkZAIDDxAPFgYeDURhdGFUZXh0RmllbGQFCVN0YXRlTmFtZR4ORGF0YVZhbHVlRmllbGQFCVN0YXRlTmFtZR4LXyFEYXRhQm91bmRnZBAVERAtLVNlbGVjdCBTdGF0ZS0tBUpPSE9SBUtFREFICEtFTEFOVEFOBk1FTEFLQQ9ORUdFUkkgU0VNQklMQU4GUEFIQU5HDFBVTEFVIFBJTkFORwVQRVJBSwZQRVJMSVMIU0VMQU5HT1IKVEVSRU5HR0FOVQVTQUJBSAdTQVJBV0FLIFdJTEFZQUggUEVSU0VLVVRVQU4gS1VBTEEgTFVNUFVSGldJTEFZQUggUEVSU0VLVVRVQU4gTEFCVUFOHVdJTEFZQUggUEVSU0VLVVRVQU4gUFVUUkFKQVlBFREQLS1TZWxlY3QgU3RhdGUtLQVKT0hPUgVLRURBSAhLRUxBTlRBTgZNRUxBS0EPTkVHRVJJIFNFTUJJTEFOBlBBSEFORwxQVUxBVSBQSU5BTkcFUEVSQUsGUEVSTElTCFNFTEFOR09SClRFUkVOR0dBTlUFU0FCQUgHU0FSQVdBSyBXSUxBWUFIIFBFUlNFS1VUVUFOIEtVQUxBIExVTVBVUhpXSUxBWUFIIFBFUlNFS1VUVUFOIExBQlVBTh1XSUxBWUFIIFBFUlNFS1VUVUFOIFBVVFJBSkFZQRQrAxFnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgsPFgIfAmhkAg0PFgIeA3NyYwUeL1B1Ymxpc2hpbmdJbWFnZXMvYnV0dG9uX2wuZ2lmZAIPDxYCHgVzdHlsZQU1YmFja2dyb3VuZC1pbWFnZTp1cmwoL1B1Ymxpc2hpbmdJbWFnZXMvYnV0dG9uX20uZ2lmKTtkAhEPFgIfBgUeL1B1Ymxpc2hpbmdJbWFnZXMvYnV0dG9uX3IuZ2lmZAIID2QWAgIBD2QWBGYPZBYCAgEPFgIfAmgWAmYPZBYEAgIPZBYGAgEPFgIfAmhkAgMPFggeE0NsaWVudE9uQ2xpY2tTY3JpcHQFhQFqYXZhU2NyaXB0OkNvcmVJbnZva2UoJ1Rha2VPZmZsaW5lVG9DbGllbnRSZWFsJywxLCAzOSwgJ2h0dHBzOlx1MDAyZlx1MDAyZnd3dy5hbWJhbmtncm91cC5jb21cdTAwMmZlbmdcdTAwMmZMb2NhdG9yJywgLTEsIC0xLCAnJywgJycpHhhDbGllbnRPbkNsaWNrTmF2aWdhdGVVcmxkHihDbGllbnRPbkNsaWNrU2NyaXB0Q29udGFpbmluZ1ByZWZpeGVkVXJsZB4MSGlkZGVuU2NyaXB0BSJUYWtlT2ZmbGluZURpc2FibGVkKDEsIDM5LCAtMSwgLTEpZAIFDxYCHwJoZAIDDw8WCh4JQWNjZXNzS2V5BQEvHg9BcnJvd0ltYWdlV2lkdGgCBR4QQXJyb3dJbWFnZUhlaWdodAIDHhFBcnJvd0ltYWdlT2Zmc2V0WGYeEUFycm93SW1hZ2VPZmZzZXRZAusDZGQCAQ9kFgQCBQ9kFgICAQ8QFgIfAmhkFCsBAGQCBw9kFgJmD2QWAmYPFCsAA2RkZGQCCg9kFgICAw9kFgJmDxYCHwALKwQBZBgBBTVjdGwwMCRtJGdfNWUwZDkzZmNfYzdiY180OTQ4XzlmNDFfMDExNThjOGZmYjVlJGdyZEFUTQ8UKwADZwL/////DwL/////D2SEbm/OSdykTzZUGp0xwdTEyKlP5w==',
                '__EVENTVALIDATION': '/wEWFALIzomvDwKghJfLCwKi/ozeBwKHk6ngDgKS2qe/AQKc2r+4DwLH47bpAwLw/8jnBALDzoZ9ApH0geIJApP0uasFApSb8akOAonkpwkCxeL2uQoCw/nz4A4CrMvkkQUC95i28wsC1/L+qw8C/YzjmQkChrz6rghHMpgkLUUfED/xK++GP0olU7mdzA==',
                'ctl00$m$g_5e0d93fc_c7bc_4948_9f41_01158c8ffb5e$ddlState': state,
                'ctl00$m$g_5e0d93fc_c7bc_4948_9f41_01158c8ffb5e$txtSearchKeyword': '',
                '__spText1': '',
                '__spText2': '',
                '_wpcmWpid': '',
                'wpcmVal': '',
            }
            yield scrapy.FormRequest(
                url = self.url,
                callback = self.detail_parse,
                method = "POST",
                formdata= data,
                
            )
    def detail_parse(self,response):
        root = html.fromstring(response.text)
        print(root)


          


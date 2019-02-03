from scrapy.http import HtmlResponse
from selenium import webdriver
import os
import platform


class JsDownloaderMiddleWare(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        oper_system = platform.system().lower()
        if oper_system == 'windows':
            rel_path = os.path.abspath('../../drivers/chromedriver_win.exe')

        elif oper_system == 'darwin':
            rel_path = os.path.abspath('../../drivers/chromedriver_mac')

        else:
            raise Exception("Operating system not supported for js execution")

        self.driver = webdriver.Chrome(chrome_options=options, executable_path=rel_path)

    def process_request(self, request, spider):
        if not request.meta['js_enabled']:
            return
        self.driver.get(request.url)
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        return response

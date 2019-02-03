import scrapy
from scrapy.crawler import CrawlerProcess
from midi_crawler.items import MidiMeta

MIDI_SIG = "4d546864"


def is_midi_file(file_bytes):
    return MIDI_SIG == file_bytes.hex()[:8]


class MidiSpider(scrapy.Spider):

    name = "Midi Spider"
    allowed_domains = [
        "midiworld.com"
    ]

    custom_settings = {
        'CONCURRENT_ITEMS': 100,
        'CONCURRENT_REQUESTS': 16,
        'DEPTH_LIMIT': 0,
        'DEPTH_STATS_VERBOSE': True,

        'DOWNLOADER_MIDDLEWARES': {
            'midi_crawler.middlewares.JsDownloaderMiddleWare': 1
        },

        'ITEM_PIPELINES': {
            'midi_crawler.pipelines.YamlWriterPipeline': 1
        },

        'JOBDIR': "persist"
    }

    def __init__(self):
        self.js_enabled = False

    def start_requests(self):
        urls = [
            "http://www.midiworld.com"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'js_enabled': self.js_enabled})

    def parse(self, response):
        if is_midi_file(file_bytes=response.body):
            file_type = "midi"
            midi_item = MidiMeta(name=file_type, content=response.body, url=response.url)
            yield midi_item

        else:
            for link in response.css('a::attr(href)'):
                yield response.follow(link, callback=self.parse, meta={'js_enabled': self.js_enabled})

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MidiSpider)
process.start()

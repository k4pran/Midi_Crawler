import scrapy
from scrapy.crawler import CrawlerProcess

MIDI_SIG = "4d546864"


def is_midi_file(file_bytes):
    return MIDI_SIG == file_bytes.hex()[:8]


class MidiSpider(scrapy.Spider):

    name = "Midi Spider"

    custom_settings = {
        'SOME_SETTING': 'some value',
    }

    def __init__(self):
        self.completed = set()
        self.target_files_found = 0

    def start_requests(self):
        urls = [
            "http://www.midiworld.com"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        self.completed.add(response.url)
        file_type = "Unknown"
        if is_midi_file(file_bytes=response.body):
            file_type = "midi"
            self.target_files_found += 1

        else:
            print("Crawling " + response.url + '...')
            for link in response.css('a::attr(href)'):
                if link in self.completed:
                    continue
                yield response.follow(link, callback=self.parse)
            print("Finished crawling " + response.url)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MidiSpider)
process.start()

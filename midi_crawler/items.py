from scrapy import Item, Field


class MidiMeta(Item):
    name = Field()
    content = Field()
    url = Field()

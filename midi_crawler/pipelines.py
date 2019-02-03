import os
import yaml


class YamlWriterPipeline(object):

    def __init__(self):
        self.items = []
        self.save_freq = 100
        self.file = None

    def open_spider(self, spider):
        self.file = open("../../record/" + "midis" + ".yaml", "a")

    def close_spider(self, spider):
        self.save_yaml()
        self.file.close()

    def process_item(self, item, spider):
        self.items.append({'name': item.get('name'), 'url': item.get('url')})
        if len(self.items) % self.save_freq == 0:
            self.close_spider(spider)

    def save_yaml(self):
        self.file.write(yaml.dump(self.items))


class ContentWriterPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not item:
            return
        filename = item['name']
        with open("../../results/" + filename + ".midi", "wb") as filename:
            filename.write(item['content'])

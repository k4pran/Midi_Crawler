

class YamlWriterPipeline(object):

    def open_spider(self, spider):
        pass
        # todo open file

    def close_spider(self, spider):
        pass
        # todo close file

    def process_item(self, item, spider):
        print(item)
        # todo Append to file
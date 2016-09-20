import json


class HabrPipeline(object):
    def __init__(self):
        self.file = open('habr.json', 'wb')

    def write(self, text):
        self.file.write(bytes(text, 'UTF-8'))

    def open_spider(self, spider):
        self.write("[\n")

    def close_spider(self, spider):
        self.write("]")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.write(line)
        return item

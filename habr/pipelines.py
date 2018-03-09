class HabrPipeline(object):
    def process_item(self, item, spider):
        item['title'] = item['title'].upper()
        item['author'] = 'Ув, {}'.format(item['author'])
        return item

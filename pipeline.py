from scrapy.exporters import JsonItemExporter
from scrapy import Item, Field


class DocItem(Item):
    """
    Item class for documentation data.
    """
    api_docs = Field()
    explanatory_text = Field()


class JsonExportPipeline:
    """
    Pipeline to export items as a JSON file.
    """
    def __init__(self):
        self.file = open("output/items.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

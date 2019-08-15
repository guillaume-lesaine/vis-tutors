# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import time
import re

class TreatmentPipeline(object):

    def process_item(self, item, spider):
        return item

class JsonLinesExportPipeline(object):

    def open_spider(self, spider):
        self.unit_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.unit_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _exporter_for_item(self, item):
        unit = ""

        search_topic = item["search_topic"]
        search_location = item["search_location"]
        teacher = item["teacher"]
        unit = "-".join([search_topic, search_location])

        full_search_date = time.strftime("%Y-%m-%d")

        export_name = f'{search_topic}_{full_search_date}_{search_location.lower()}.json'

        if unit not in self.unit_to_exporter:
            f = open(f"./data/scraper/{full_search_date}/{export_name}", 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.unit_to_exporter[unit] = exporter
        
        return self.unit_to_exporter[unit]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item

import re
import json
from collections import defaultdict

class AuditParser:
    def __init__(self):
        pass


    def parse(self, text):
        matches = re.findall(r"<custom_item>([\S\s]*?)</custom_item>", text)
        custom_items = []

        types = defaultdict(lambda: 0)

        for inner_text in matches:
            custom_item = {}
            pattern = re.compile(r'^[\s]+([a-z_]+)\s+:\s+([^\n]+)',re.MULTILINE)
            matches = pattern.findall(inner_text)

            for property, val1 in matches:
                custom_item[property] = val1

                if property == 'type':
                    types[custom_item[property]] += 1


            custom_items.append(custom_item)
        print(types)

        return json.dumps(custom_items)
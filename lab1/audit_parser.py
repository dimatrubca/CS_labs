import re
import json

class AuditParser:
    def __init__(self):
        pass


    def parse(self, text):
        matches = re.findall(r"<custom_item>([\S\s]*?)</custom_item>", text)
        custom_items = []

        for inner_text in matches:
            custom_item = {}
            pattern = re.compile(r'^[\s]+([a-z_]+)\s+:\s+(("[\S\s\n]*?")|([^\n]+))',re.MULTILINE)
            matches = pattern.findall(inner_text)

            for property, val1, val2, _ in matches:
                if val1:
                    custom_item[property] = val1
                else:
                    custom_item[property] = val2

            custom_items.append(custom_item)

        return json.dumps(custom_items)
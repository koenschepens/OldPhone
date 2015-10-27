import xml.etree.ElementTree as ET
import os


def getText(id, filename='default.xml', lang='en'):
    tree = ET.parse(os.path.join(os.path.dirname(__file__), lang, filename))
    root = tree.getroot()
    for item in root.findall('string[@id="' + str(id) + '"]'):
        return item.text
    return "Not found"

import re

XML_ID = re.compile(r"id=\"(.+?)\"")
XML_TEXT_SIMPLE = re.compile(r"<text>(.*)</text>")
XML_TEXT_MULTILINE_START = re.compile(r"<text>(.*)")
XML_TEXT_MULTILINE_END = re.compile(r"(.*)</text>")


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))

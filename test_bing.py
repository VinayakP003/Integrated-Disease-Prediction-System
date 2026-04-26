import urllib.request
import urllib.parse
from html.parser import HTMLParser
import re

class BingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_snippet = False
        self.snippets = []
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        if tag in ["div", "p"]:
            for attr in attrs:
                if attr[0] == "class" and attr[1] and ("b_algoSlug" in attr[1] or "b_caption" in attr[1]):
                    self.in_snippet = True

    def handle_endtag(self, tag):
        if self.in_snippet and tag in ["div", "p"]:
            self.in_snippet = False
            text = "".join(self.current_data).strip()
            if text:
                self.snippets.append(text)
            self.current_data = []

    def handle_data(self, data):
        if self.in_snippet:
            self.current_data.append(data)

def get_review_snippet(query):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            parser = BingParser()
            parser.feed(html)
            return parser.snippets
    except Exception as e:
        return [str(e)]

res = get_review_snippet('Dr. Michael Chen Cardiologist San Francisco review "patient"')
print("Snippets:")
for r in res:
    print("-", r.replace('\n', ' '))

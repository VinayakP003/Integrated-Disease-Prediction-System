import urllib.request
import urllib.parse
from html.parser import HTMLParser

class DDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.titles = []
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "class" and "result__a" in attr[1]:
                    self.in_title = True

    def handle_endtag(self, tag):
        if self.in_title and tag == "a":
            self.in_title = False
            text = "".join(self.current_data).strip()
            if text:
                self.titles.append(text)
            self.current_data = []

    def handle_data(self, data):
        if self.in_title:
            self.current_data.append(data)

query = "dr Cardiologist New York site:healthgrades.com/physician"
url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
req = urllib.request.Request(
    url, 
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
)
with urllib.request.urlopen(req, timeout=5) as response:
    html = response.read().decode('utf-8')
    parser = DDGParser()
    parser.feed(html)
    print(parser.titles)

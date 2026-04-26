import urllib.request
import urllib.parse
from html.parser import HTMLParser

class RobustDDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_snippet = False
        self.current_title = []
        self.current_snippet = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "class" and "result__snippet" in attr[1]:
                    self.in_snippet = True
                if attr[0] == "class" and "result__url" in attr[1]:
                    self.in_title = True

    def handle_endtag(self, tag):
        if tag == "a":
            if self.in_snippet:
                self.results.append("SNIPPET: " + "".join(self.current_snippet).strip())
                self.current_snippet = []
                self.in_snippet = False
            if self.in_title:
                self.results.append("TITLE: " + "".join(self.current_title).strip())
                self.current_title = []
                self.in_title = False

    def handle_data(self, data):
        if self.in_snippet:
            self.current_snippet.append(data)
        if self.in_title:
            self.current_title.append(data)

def spoof_scrape():
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote("top Cardiologists San Francisco healthgrades")
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            html = r.read().decode('utf-8')
            parser = RobustDDGParser()
            parser.feed(html)
            return parser.results
    except Exception as e:
        return [str(e)]

print(spoof_scrape())

import urllib.request
import urllib.parse
from html.parser import HTMLParser

class DDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_snippet = False
        self.snippets = []
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "a" and "result__snippet" in attrs_dict.get("class", ""):
            self.in_snippet = True

    def handle_endtag(self, tag):
        if self.in_snippet and tag == "a":
            self.in_snippet = False
            text = "".join(self.current_data).strip()
            if text:
                self.snippets.append(text)
            self.current_data = []

    def handle_data(self, data):
        if self.in_snippet:
            self.current_data.append(data)

def test_scrape():
    doctor_name = "Dr. Samin Sharma"
    location = "New York"
    query = f'"{doctor_name}" {location} patient google reviews'
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            parser = DDGParser()
            parser.feed(html)
            print(f"Found {len(parser.snippets)} snippets")
            for i, snip in enumerate(parser.snippets):
                print(f"{i}: {snip}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_scrape()

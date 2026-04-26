from duckduckgo_search import DDGS

def raw_scrape():
    try:
        with DDGS() as ddgs:
            results = ddgs.text("site:healthgrades.com Cardiologist San Francisco review", max_results=3)
            for r in results:
                print(r)
    except Exception as e:
        print("ERROR:", e)

raw_scrape()

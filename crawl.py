import crawler.crawler
obj = crawler.crawler.crawler()
inp1 = input("Website to crawl: ")
inp2 = input("Level to crawl (0 for default): ")
crawler.crawler.start_url = inp1
crawler.crawler.end_level = int(inp2)
obj.crawl()

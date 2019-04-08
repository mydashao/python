from scrapy import cmdline

cmdline.execute("scrapy crawl quotes -o quotes.csv".split())

import scrapy 
from scrapy.crawler import CrawlerProcess

class SoccerSpider(scrapy.Spider):
    name = 'soccer_spider'

    def start_requests(self):
        urls = ["https://www.football-data.co.uk/mmz4281/2425/B1.csv"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        csv_file = 'JupilerLeagueLatest.csv'
        with open(csv_file, 'wb') as file:
            file.write( response.body )

def release_the_spider():
    process = CrawlerProcess()
    process.crawl(SoccerSpider)
    process.start()

release_the_spider()
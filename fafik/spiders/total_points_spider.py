import scrapy
import scrapy_splash
import csv


class QuotesSpider(scrapy.Spider):
    name = "total_points"

    def start_requests(self):
        urls = [
                'https://fantasy.premierleague.com/a/statistics/total_points#2'
        ]
        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        pass
        with open('out.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerows([[td.extract() for td in row.css('td a.ismjs-show-element::text,td:not(.ism-table--el__status):not(.ism-table--el__primary)::text')] for row in response.css("tr")])



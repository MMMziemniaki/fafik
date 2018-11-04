import scrapy
import csv
import json


class TotalPointsSpider(scrapy.Spider):
    name = "total_points"

    def start_requests(self):
        urls = [
                'https://fantasy.premierleague.com/drf/bootstrap-static'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open('out.json', 'w') as f:
            f.write(response.text)
        data = json.loads(response.text)
        data['elements'].sort(reverse = True, key = lambda player : player['total_points'])
        with open('out.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Cost', 'Selected by', 'Form', 'Points']);
            writer.writerows([[player['web_name'], player['now_cost'], player['selected_by_percent'], player['form'], player['total_points']] for player in data['elements']])

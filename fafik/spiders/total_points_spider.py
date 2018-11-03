import scrapy
import scrapy_splash
import csv


class TotalPointsSpider(scrapy.Spider):
    name = "total_points"

    lua_script = """
    function tablesToString(tables)
        local ret = ""
        for _, value in ipairs(tables)
        do
            ret = ret .. value .. '\\n'
        end

        return ret
    end

    function main(splash)
        assert(splash:go(splash.args.url))
        local tables = {}
        repeat
            local pageNumber = splash:select('p.ism-pagination__info strong')
            assert(pageNumber)
            print("Page number " .. pageNumber:text())

            tables[tonumber(pageNumber:text())] = splash:select('table'):info().html
            assert(tables[tonumber(pageNumber:text())])

            local button = splash:select('a.paginationBtn:nth-child(4):not(.paginationBtn.inactive)')
            if button then
                assert(button:mouse_click())
            end
        until not button

        return tablesToString(tables)
    end
    """

    def start_requests(self):
        urls = [
                'https://fantasy.premierleague.com/a/statistics/total_points'
        ]
        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': TotalPointsSpider.lua_script})

    def parse(self, response):
        with open('out.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerows([[td.extract() for td in row.css('td a.ismjs-show-element::text,td:not(.ism-table--el__status):not(.ism-table--el__primary)::text')] for row in response.css('tr') if row.css('td')])



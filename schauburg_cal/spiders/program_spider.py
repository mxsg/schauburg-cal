import scrapy
import datetime

class ProgramSpider(scrapy.Spider):
    name = "program"
    allowed_domains = ["schauburg.de"]
    start_urls = ["http://schauburg.de/programm.php"]

    def parse(self, response):
        dates = response.xpath('/html/body/h5/text()').extract()
        movieLists = response.xpath('/html/body/table')

        # print dateSelector.extract(), movieListSelector.extract()

        for dateText, movies in zip(dates, movieLists):
            # the date string is preceded by the day of the week
            # dateText should contain the date in "DD.MM." format
            dateText = dateText.split(',')[-1].strip().split('.')
            day = int(dateText[0])
            month = int(dateText[1])

            today = datetime.date.today()

            # find out correct year for the program:
            # date with shortest difference to today is probably the right one
            dateThisYear = datetime.date(today.year, month, day)
            dateNextYear = datetime.date(today.year + 1, month, day)

            diffThisYear = abs(dateThisYear - today)
            diffNextYear = abs(dateNextYear - today)

            # construct scrapy item
            date = dateThisYear if diffThisYear < diffNextYear else dateNextYear
            print date

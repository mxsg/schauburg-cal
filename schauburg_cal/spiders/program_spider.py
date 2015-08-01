import scrapy
import datetime
import urlparse
import pytz

from schauburg_cal.items import MovieShowing

class ProgramSpider(scrapy.Spider):
    name = "program"
    allowed_domains = ["schauburg.de"]
    start_urls = ["http://schauburg.de/programm.php"]
    base_url = "http://schauburg.de"

    def parse(self, response):
        dates = response.xpath('/html/body/h5/text()').extract()
        movieLists = response.xpath('/html/body/table')

        # print dateSelector.extract(), movieListSelector.extract()

        for dateText, movies in zip(dates, movieLists):

            # construct scrapy item
            showing = MovieShowing()


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

            movieEntrySelectors = movies.xpath('tr')

            for movieEntry in movieEntrySelectors:

                tableCells = movieEntry.xpath('td')

                # add time zone information to time
                tzBerlin = pytz.timezone('Europe/Berlin')

                showingTime = tableCells.xpath('text()').extract_first().split('.')
                showingDatetimeNaive = datetime.datetime(date.year, date.month, date.day,
                        int(showingTime[0]), int(showingTime[1]))

                showing['dateTime'] = tzBerlin.localize(showingDatetimeNaive)


                showing['name'] = tableCells.xpath('a/text()').extract_first().strip()
                showing['url'] = urlparse.urljoin(self.base_url,
                        tableCells.xpath('a/@href').extract_first())

                showing['comment'] = tableCells.xpath('i/text()').extract_first()

                yield showing

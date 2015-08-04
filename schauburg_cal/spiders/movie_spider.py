import scrapy
import datetime
import urlparse
import pytz
import re

from schauburg_cal.items import MovieShowing

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["schauburg.de"]
    start_urls = ["http://schauburg.de/programm.php"]
    base_url = "http://schauburg.de"

    def parse(self, response):
        linkParts = response.xpath('/html/body/table/tr/td/a/@href').extract()

        for link in linkParts:
            fullURL = urlparse.urljoin(self.base_url, link)
            yield scrapy.Request(fullURL, callback=self.parseFilmPage)

    def parseFilmPage(self, response):

        # construct movie item
        showing = MovieShowing()

        showing['url'] = response.url

        contentSelector = response.xpath('/html/body/center/table/tr/td/table/tr/td')

        movieTitle = contentSelector.xpath('h4/text()').extract_first().strip()
        showing['name'] = movieTitle

        paragraphs = filter(len, [paragraph.strip()
                for paragraph in contentSelector.xpath('//p[@class="Text"]/text()').extract()])
        showing['description'] = '\n'.join(paragraphs)

        dataLines = filter(len, [paragraph.strip()
                for paragraph in contentSelector.xpath('//p[@class="Daten"]/text()').extract()])
        showingData = '\n'.join(dataLines)
        showing['data'] = showingData

        # parse film length
        reLength = re.compile(r'(\b\d+)\s+Minuten')
        m = reLength.search(showingData)

        if m:
            try:
                length = int(m.group(1))
                showing['length'] = length
            except:
                showing['length'] = None

        # now parse movie showing information

        for dateRowSel in contentSelector.xpath('table[@class="Spielzeiten"][1]/tr'):
            dateString = dateRowSel.xpath('td[1]/i/text()').extract_first()
            dateRE = re.compile(r'\w+\s+(\d+)[.](\d+)[.](\d+):', re.UNICODE)
            m = dateRE.match(dateString)

            movieDate = None
            if m:
                day = int(m.group(1))
                month = int(m.group(2))
                year = int('20' +m.group(3))
                movieDate = datetime.date(year, month, day)
            else:
                print "*** Error while parsing showing date. ***"
                print dateString

            showings = dateRowSel.xpath('td[2]/text()').extract_first().split('+')

            for movieTime in showings:
                movieTimeRE = re.compile(r'(\d+)[.](\d+)\s+Uhr(?:\s+\((.*)\))?', re.UNICODE)
                m = movieTimeRE.match(movieTime.strip())

                if not m:
                    print "*** Error while parsing showing time. ***"
                    print movieTime

                # add time zone information to time
                tzBerlin = pytz.timezone('Europe/Berlin')

                showingDatetimeNaive = datetime.datetime(year, month, day,
                        int(m.group(1)), int(m.group(2)))

                showing['dateTime'] = tzBerlin.localize(showingDatetimeNaive)

                showing['comment'] = m.group(3)

                yield showing

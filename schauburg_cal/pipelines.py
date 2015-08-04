# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import icalendar
import datetime
import pytz

class SchauburgICalExportPipeline(object):

    def open_spider(self, spider):
        self.cal = icalendar.Calendar()
        # TODO: create real prodid
        self.cal.add('prodid', '-//mxsg//schauburg_cal//DE')
        self.cal.add('version', '2.0')

    def process_item(self, showing, spider):
        event = icalendar.Event()
        event.add('summary', showing['name'])

        startdt = showing['dateTime'].astimezone(pytz.utc)

        if 'length' in showing:
            enddt = startdt + datetime.timedelta(minutes=showing['length'])
        else:
            enddt = startdt + datetime.timedelta(hours=2)

        event.add('dtstart', startdt)
        event.add('dtend', enddt)
        event.add('dtstamp', datetime.datetime.now())

        # put movie URL in description field
        event.add('url', showing['url'])

        comment = showing['comment']
        print comment

        if comment is not None:
            print comment
            event.add('description', comment)

        print "Writing event to calendar..."
        self.cal.add_component(event)

        return showing

    def close_spider(self, spider):

        with open('schauburg.ics', 'w') as f:
            f.write(self.cal.to_ical())


class SchauburgCalPipeline(object):
    def process_item(self, item, spider):
        return item

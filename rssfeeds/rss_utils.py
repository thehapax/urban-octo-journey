from reader import make_reader, FeedExistsError
import calendar
import datetime
from datetime import date
from dateutil import relativedelta
import yaml
from bs4 import BeautifulSoup
import re
import pandas as pd

# basic methods for adding, update and getting rss feeds
def add_and_update_feed(feed_url, reader):
    try:
        reader.add_feed(feed_url)
    except FeedExistsError:
        pass
    reader.update_feeds()


def next_month():
    ''' returns next month and year in this format, if current month is
        September 2020 (2020, 9): (2020, 10)
    '''
    # usage: 10 = nextmonth.month, 2020 = nextmonth.year
    nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)
    return nextmonth

# if its a meetup rss feed
# get the date and return it - word before and after the month. 
# in between the <p></p>, e.g. <p>Tuesday, September 22 at 6:15 PM</p>
def check_month(summary, month):    
    soup = BeautifulSoup(summary, 'html.parser')
    event_date = None
    this_month = calendar.month_name[month]
    short_month = calendar.month_abbr[month]
    if (summary.__contains__(short_month)) or (summary.__contains__(this_month)):
        #print("Short Month MATCH")  # check if there are "Sep"
        for link in soup.find_all('p'):
            link_string = str(link.string)
            if (this_month in link_string) or (short_month in link_string):
                event_date = link_string

    if event_date is not None:
        return event_date
    else:
        return False
    

def check_event_number(eventlink):
    '''
     as of Sept 2020, random meetup event number is 272799202
     check to make sure that the current events numbers are greater
     in case we have wrap around events from previous years. 
    '''
    if "meetup.com" in eventlink: 
        match = re.findall('[0-9]+', eventlink)
        if match:
            eventnum = int(match[0])
            if eventnum > 270700100:
                print(str(eventnum) + " > min threshold")
                return True
            else:
                # not sure this is the right way to handle issue
                print(str(eventnum) + " < OBSOLETE or NULL? " + eventlink)
                return False
        

# get latests that have not been read and post them 
# after posting then mark as read
def get_latest(reader, current):
    today = None
    if current:
        today = date.today()
    else: 
        today = next_month()
    
    entries = list(reader.get_entries(read=False))    
    rows = []
    
    for entry in entries:
        #print(entry.summary)
        currdate = check_month(entry.summary, today.month)
        #eventdate = check_event_number(entry.link)
        #if currdate and eventdate:
        this_month = calendar.month_name[today.month]
        if currdate:
            edate = currdate.split('at')[0]
            shortdate = int(edate.split(this_month)[1])
            row = (shortdate, edate, entry.title, entry.link)
            rows.append(row)
    frame = pd.DataFrame(rows, columns=['ShortDate', 'FullDate', 'EventName', 'Link'])
    result = frame.sort_values(by='ShortDate', ascending=True)
    print(result)
    return result

    #reader.mark_as_read(entry)


def get_rss_config():
    path  = "./"
    config_file = path + 'rss.yml'
    with open(config_file, 'rb') as f:
        config = yaml.safe_load(f)
    return config


'''
if __name__ == "__main__":
    config = get_rss_config()
    feedlist = config["feedlist"]
    print(feedlist)

    reader = make_reader("db.sqlite")
    for f in feedlist: 
        add_and_update_feed(f) 
        feed = reader.get_feed(f)
        print(f"updated {feed.title} (last changed at {feed.updated})\n")

    # make this an hourly cron job
    result = get_latest(reader)
    print(result)
'''
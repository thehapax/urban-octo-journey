from telethon import TelegramClient, events, sync, utils, functions
import yaml
import sys
import logging
import aiocron
import asyncio
from reader import make_reader, FeedExistsError
from utils import split_sponsored, get_ids, get_inbound, get_name, get_myinfo
from rss_utils import add_and_update_feed, get_latest
import pandas as pd    

# consolidate RSS feeds to a telegram chat group or channel
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)


path  = "./"
config_file = path + 'rss.yml'
with open(config_file, 'rb') as f:
    config = yaml.safe_load(f)
        
# We have to manually call "start" if we want an explicit bot token
# with actual user account - oc
client = TelegramClient(config["session_name"], 
                        config["api_id"], 
                        config["api_hash"])

##### get inbound chat group streams if any ######
inbound_groups = get_inbound(config)

##### single outbound stream ######
outbound = config['outbound']
#print(f'Outbound Feed: {outbound}')
client.parse_mode = 'html'
client.start()

feedlist = config["feedlist"]
#print(feedlist)

reader = make_reader("db.sqlite")
# run on startup and as daily cron job to update feeds
'''
for f in feedlist: 
    add_and_update_feed(f, reader) 
    feed = reader.get_feed(f)
    print(f"updated {feed.title} (last changed at {feed.updated})\n")
'''

# get_myinfo(client) # get your info for setting up config.yml
this_month = True
result = get_latest(reader, this_month)
print(result)
print(" END running get latest initial.... ")


# listen to chat groups and forward messsages
@client.on(events.NewMessage(chats=inbound_groups))
async def msghandler(event):
    try:
        sender = await event.get_sender()
        username = sender.username
        name = get_name(sender)
        inbound = "<b>" + name + "</b>\n\n"
        logger.info(inbound)

        inbound_message = "<b>" + username + "</b>\n\n"
        body_msg = split_sponsored(event.message.text)  # remove sponsored msg
        inbound_message = inbound_message + body_msg
        if body_msg is not None:
            await client.send_message(outbound, inbound_message, parse_mode='html')

        if event.message.media is not None:
            # don't announce source, just forward the media
            await client.send_file(outbound, event.message.media, force_document=True)
    except Exception as e:
        logger.error(e)


@aiocron.crontab('* * * * *') 
async def poll_rssfeeds():
    this_month = True
    result = get_latest(reader, this_month)
    print(" running rss feed cron job .... ")
    for index, r in result.iterrows():
        entry = r['FullDate'] + "\n" + r['EventName'] + "\n" + r['Link'] + "\n\n"
        await client.send_message(outbound, entry,  link_preview=False)
    

# run as daily cron job to update feeds
# */2 is every 2nd minute, 30 is every hour at 30 min mark
@aiocron.crontab('0 0 * * *') 
async def update_feeds():
    for f in feedlist: 
        add_and_update_feed(f, reader) 
        feed = reader.get_feed(f)
        print(f"updated {feed.title} (last changed at {feed.updated})\n")
        

############
client.run_until_disconnected()


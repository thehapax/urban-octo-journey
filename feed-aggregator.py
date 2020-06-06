from telethon import TelegramClient, events, sync, utils, functions
import yaml
import sys
import logging
from utils import split_sponsored

### this script will consolidate multiple channels to one channel/group/user on telgram
# source code examples from https://docs.telethon.dev/en/latest/basic/quick-start.html
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

def get_ids(client):
    # You can print all the dialogs/conversations that you are part of:
    for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


def get_inbound(config):
    inbounds = config['inbound_streams']
    print(f'Inbound Feeds: {inbounds}')
    return inbounds


def main(config):
    # We have to manually call "start" if we want an explicit bot token
    # with actual user account - octocubic
    client = TelegramClient(config["session_name"], 
                            config["api_id"], 
                            config["api_hash"])

    ##### get inbound streams ######
    inbound_groups = get_inbound(config)

    ##### single outbound stream ######
    outbound = config['outbound']
    print(f'Outbound Feed: {outbound}')
    client.parse_mode = 'html'
    client.start()

    # Getting information about yourself
    me = client.get_me()
    # print(me.stringify())
    # username = me.username
    # print(username)
    # get_ids(client)  # prints out all IDs of chats and channels user is in.
    
    # listen and send messsages
    @client.on(events.NewMessage(chats=inbound_groups))
    async def handler(event):
        sender = await event.get_sender()
        username = sender.username
        inbound_message = "<b>" +  username + "</b>\n\n"
        body_msg = split_sponsored(event.message.text) # remove sponsored msg
        inbound_message = inbound_message + body_msg
#        print(inbound_message)
        await client.send_message(outbound, inbound_message, parse_mode='html')

    client.run_until_disconnected()
     

if __name__ == "__main__":
    path  = "./"
    config_file = path + 'config.yml'
    with open(config_file, 'rb') as f:
        config = yaml.safe_load(f)
    main(config)

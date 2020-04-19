from telethon import TelegramClient, events, sync, utils, functions
import yaml
import sys
import logging

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
    client.start()

    # Getting information about yourself
    me = client.get_me()
    # print(me.stringify())
    # username = me.username
    # print(username)
    # get_ids(client)
    
    # listen and send messsages
    @client.on(events.NewMessage(chats=inbound_groups))
    async def handler(event):
        inbound_message = event.message.raw_text
        await client.send_message(outbound, inbound_message)

    client.run_until_disconnected()
     

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)
    main(config)

import logging

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


def get_name(sender):
    name = ""
    try:
        first_name = sender.first_name
        last_name = sender.last_name
        if first_name is not None:
            name = first_name
            if last_name is not None:
                name = name + "  " + last_name
        elif last_name is not None:
            name = last_name
    except Exception as e:
        logger.error(e)
    return name
    

# remove all content that is SPONSORED
def split_sponsored(msg):
    if "SPONSORED" in msg:
        marr = msg.split("SPONSORED")
        return marr[0]
    else:
        return msg


if __name__ == "__main__":
        
    f = open("sample.txt", "r")
    content = f.read()

    result  = split_sponsored(content)
    print(result)

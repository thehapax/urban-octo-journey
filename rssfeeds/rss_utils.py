from reader import make_reader, FeedExistsError
import yaml

# basic methods for adding, update and getting rss feeds

def add_and_update_feed(feed_url, reader):
    try:
        reader.add_feed(feed_url)
    except FeedExistsError:
        pass
    reader.update_feeds()

# get latests that have not been read and post them 
# after posting then mark as read
def get_latest(reader):
    entries = list(reader.get_entries(read=False))
    result = []
    for entry in entries:
        print(entry)
        msg = ""
        msg = "<b>" + entry.title + "</b>\n\n" + entry.link + "\n"
        #  + entry.summary + "\n" 
        #reader.mark_as_unread(entry)
        #reader.mark_as_read(entry)
        result.append(msg)
    return result


def get_rss_config():
    path  = "./"
    config_file = path + 'rss.yml'
    with open(config_file, 'rb') as f:
        config = yaml.safe_load(f)
    return config


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
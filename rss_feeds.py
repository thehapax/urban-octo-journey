from reader import make_reader, FeedExistsError
import yaml

def add_and_update_feed(feed_url):
    try:
        reader.add_feed(feed_url)
    except FeedExistsError:
        pass
    reader.update_feeds()


def get_config():
    path  = "./"
    config_file = path + 'rss.yml'
    with open(config_file, 'rb') as f:
        config = yaml.safe_load(f)
    return config


def get_latest(reader):
    entries = list(reader.get_entries(read=False))
    result = ''
    for entry in entries:
        msg = "---------\n"
        msg = msg + entry.title + "\n" + entry.link + "\n"
    #    reader.mark_as_read(entry)
        result = result + msg
    return result


if __name__ == "__main__":
    config = get_config()
    feedlist = config["feedlist"]
    print(feedlist)

    reader = make_reader("db.sqlite")
    for f in feedlist: 
        add_and_update_feed(f) 
        feed = reader.get_feed(f)
        print(f"updated {feed.title} (last changed at {feed.updated})\n")
    
    result = get_latest(reader)
    print(result)
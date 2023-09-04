from Adafruit_IO import Client, RequestError, Feed
import os


def send_price_to_ada_io(user, key, feeds, data):
    aio = Client(user, key)
    test_feed = aio.feeds(feeds)
    aio.send_data(test_feed.key, data)


if __name__ == "__main__":

    os.environ["ADAFRUIT_IO_USERNAME"] = "cccc"
    os.environ["ADAFRUIT_IO_KEY"] = "f9fc56ca88b348119a65a7063c4d1355"

    user = os.environ["ADAFRUIT_IO_USERNAME"]
    key = os.environ["ADAFRUIT_IO_KEY"]

    send_price_to_ada_io(user, key, "meeb-p", 69.1)

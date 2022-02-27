import tweepy #Library for Twitter
import json,os,datetime
import emoji

#loading credentials for the Twitter API
with open('auth.txt') as f: 
    data = f.read()
authDict = json.loads(data)
auth = tweepy.OAuthHandler(authDict['consumer_key'],authDict['consumer_secret'])
api = tweepy.API(auth)

class EmojiStreamListener(tweepy.StreamListener):
    """
    Implementation of the Abstract StreamListener object provided in the library. This library is not thread safe.
    """
    def __init__(self):
        self.cache_length = 5000
        self.cache=[]
        if not os.path.exists(os.getcwd()+"\\Tweets\\"):
            os.makedirs(os.getcwd()+"\\Tweets\\")
    def on_error(self, status_code):
        print(status_code)
    def on_status(self, status):
        """
        param: status
        takes a status, adds it to the internal cache and flushes the cache to disk if it is large enough
        No need to check emojis as it is only streaming statuses with Emojis.
        """
        self.cache.append(status.text)
        if len(self.cache)>self.cache_length:
            with open(os.getcwd()+"\\Tweets\\{0}.json".format(datetime.datetime.now().strftime("%b %d %y "
                                                                                              "%H-%M-%S%Z")),"a+") as jsonf:
                json.dump(self.cache,jsonf)

emojiStreamListener = EmojiStreamListener()
emojiStream = tweepy.Stream(auth=api.auth,listener=emojiStreamListener)
emojiList = [e for e in emoji.UNICODE_EMOJI['en'].keys()] #Getting a list of all emojis in the Emoji hashmap
emojiStream.filter(track=emojiList) #Makes sure the only statuses we get have emojis in them
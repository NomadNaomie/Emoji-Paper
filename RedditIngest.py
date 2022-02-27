import praw #Reddit Library
import json,os,datetime,threading
import emoji


class Scraper():
    def __init__(self):
        self.CACHE_LENGTH = 5000 #How many comments before flushing cache from internal memory to disk
        self.cache = []
        if not os.path.exists(os.getcwd()+"\\Archive\\NewEmoji\\"):
            os.makedirs(os.getcwd()+"\\Archive\\NewEmoji\\")
        subreddit = reddit.subreddit("all") #Targeting every comment, due to rate limit uses, will most likely miss up to 20%
        for comment in subreddit.stream.comments(skip_existing=True):
            threading.Thread(target=self.process_message,args=(comment,)).start() #Start a new thread for each comment so the execution is parallel


    def has_emoji(self,text):
        """
        param: string
        returns: boolean
        Function takes in a string and checks if any character in the text is an emoji, otherwise it returns false
        Utilises the Emoji->English name hashmap
        """
        for character in text:
            if character in emoji.UNICODE_EMOJI['en']:
                return character in emoji.UNICODE_EMOJI['en']
        return False

    def process_message(self,comment):
        """
        param: comment 
        returns: nothing
        Takes Reddit Comment PRAW object, if the comment has an emoji, if it's not the automoderator and the subreddit is not a subreddit marked for Over 18s, generally pornography subredits, then add the comment to the internal cache
        if the cache is at it's max length, write it to disk and clear the cache.
        
        """
        if self.has_emoji(comment.body) and comment.author.name!="AutoModerator" and not comment.subreddit.over18:
            self.cache.append([comment.body,"https://reddit.com"+comment.permalink])
            if (len(self.cache)==self.CACHE_LENGTH):
                timenow = datetime.datetime.utcnow().strftime("%b %d %y %H-%M-%S%Z")
                with open(os.getcwd()+"\\Archive\\NewEmoji\\"+timenow+".json","a+") as jsonf:
                    json.dump(self.cache,jsonf)
                self.cache=[]




s = Scraper()
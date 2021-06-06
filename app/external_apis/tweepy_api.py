""" Twitter API """
import tweepy

from config import Config

# set the twitter auth
auth = tweepy.OAuthHandler(Config.CONSUMER_KEY, Config.CONSUMER_SECRET)
auth.set_access_token(Config.ACCESS_TOKEN, Config.ACCESS_TOKEN_SECRET)

# create the tweepy api
api = tweepy.API(auth)

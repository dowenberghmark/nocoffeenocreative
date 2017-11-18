import tweepy
import re
import os
from twitter_credentials import *

def clean_tweet(tweet):
    tweet = re.sub("https?\:\/\/", "", tweet)   #links
    tweet = re.sub("#\S+", "", tweet)           #hashtags
    tweet = re.sub("\.?@", "", tweet)           #at mentions
    tweet = re.sub("RT.+", "", tweet)           #Retweets
    tweet = re.sub("Video\:", "", tweet)        #Videos
    tweet = re.sub("\n", "", tweet)             #new lines
    tweet = re.sub("^\.\s.", "", tweet)         #leading whitespace
    tweet = re.sub("\s+", " ", tweet)           #extra whitespace
    tweet = re.sub("&amp;", "and", tweet)       #encoded ampersands
    tweet = re.sub("t.co\S+", "", tweet)        #t.co links
    return tweet


def get_tweets(screen_name):
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    client = tweepy.API(auth)


    new_tweets = client.user_timeline(screen_name=screen_name, tweet_mode='extended', count=30000)

    os.remove('donald.txt')

    with open('donald.txt','x') as donald_file:
       for tweet in new_tweets:
          tweet = clean_tweet(tweet._json['full_text'])
          donald_file.write(tweet + '\n')

    donald_file.close()

if __name__ == '__main__':
    get_tweets('@realDonaldTrump')



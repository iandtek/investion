import os
import re
import tweepy
from textblob import TextBlob
from pprint import pprint

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
  
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except Exception as e:
            print(e)
  
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''

        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        tweet = re.sub("\\n", '', tweet)
        tweet = re.sub('https?:\/\/\S+', '', tweet)
        return tweet
  
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        result = {'polarity': analysis.polarity}

        # set sentiment
        if analysis.sentiment.polarity > 0:
            result['polarity_label'] = 'positive'
        elif analysis.sentiment.polarity == 0:
            result['polarity_label'] = 'neutral'
        else:
            result['polarity_label'] = 'negative'
        
        #get subjectivity
        result['subjectivity'] = analysis.subjectivity

        return result

  
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
  
        try:
  
            # parsing tweets one by one
            for tweet in tweepy.Cursor(self.api.search, q=query, lang="en", tweet_mode='extended').items(count):
                # empty dictionary to store required params of a tweet
                parsed_tweet = tweet._json

                parsed_tweet['clean_tweet'] = self.clean_tweet(tweet.full_text)
  
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)

                pprint(tweet._json)
  
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
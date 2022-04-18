import tweepy

consumer_key = '6TF530DVabB3XZPRlWVojAwKF'
consumer_secret = 'xakc3egwiugqF6C0oxdgCQHx58JGhl3k0buKA9aoBgU76QLqvZ'
access_token = '1449559138875363333-WFglKEaF7esj11gntiO3RBqewhhd9r'
access_token_secret = '3Engzoxos04T2ry94cNfkYmUyiA2ozkBwukMXDoJhJmP6'

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

def getTweets(topic, count):
    # tweets = getTweets(topic, count)
    # call twitter api to fetch tweets
    fetched_tweets = api.search_tweets(q = topic, count = 5000, lang="en")
    # empty list to store parsed tweets
    tweets = []
    # parsing tweets one by one
    for tweet in fetched_tweets:
        # empty dictionary to store required params of a tweet
        parsed_tweet = {}
        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['time'] = tweet.created_at
        # appending parsed tweet to tweets list
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)
    # return parsed tweets
    return tweets

def levelOfConcern(tweets):
    #get tweets for certain days as a list
    '''
    list of tweet text and date
    calculate sum of sentiment for each date
    '''



# geocode="-22.9122,-43.2302,1km"

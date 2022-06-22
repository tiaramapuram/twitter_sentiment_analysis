import tweepy #importing twitter library
import re #importing regular expressions to split string with multiple delimiters
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #imporitng setiment analyzer
import pandas as pd 

    #API key and secret key from twitter
key = 'pbJsxD8wRC0BDGuBuC4Gk8gn3'
secret = 'Dp21V6obsOL7N4hwBHoTwCR9tXy25wJyhCX22VonBcWKpbO13U'
    #logging in and establishing connection
auth = tweepy.OAuthHandler(key,secret)
api = tweepy.API(auth)
    #users whose tweets are going to be analyzed
twitter_users = ['BarackObama', 'elonmusk', 'BillGates', 'kanyewest', 'KimKardashian']
    #the positive and negative words used for analysis
goodWords = ['like', 'love', 'nice', 'sweet', 'good', 'happy', 'joy', 'yeah', 'awesome', 'wonderful', 'laugh', 'yes', 'thankful', 'great']
badWords = ['hate', 'no', 'bad', 'dirty', 'sad', 'nope', 'terrible', 'not', 'horrible', 'sucks', 'awful', 'yuck', 'nah', 'worry', 'hurt']
    #fields needed in the csv file
tweets = []
authors = []
basic_sentiment_scores = []
analyzer_scores = []
    #getting 200 tweets from each of the 5 users mentioned above
for user in twitter_users:
    tweet_data = api.user_timeline(screen_name=user,tweet_mode="extended",count=200)
    #adding the tweets into 'tweets' array and tweet authors into 'author' array
    for tweet in tweet_data:
        tweets.append(tweet.full_text)
        authors.append(tweet.author.name)

    #cleaning tweets to iterate through each word
        #changing all text to lower case
        lower_text = tweet.full_text.lower()
        #splitting the tweet to single words 
        split_tweet = re.split(' |\.|\, ',lower_text)
        gw_count = [0]
        bw_count = [0]
        #calculating good word and bad word count
        for good in goodWords:
            gw_count = gw_count + split_tweet.count(good)
        for bad in badWords:
            bw_count = bw_count + split_tweet.count(bad)
        #calculating sentiment score and adding it to array
        sentiment_score = gw_count - bw_count
        basic_sentiment_scores.append(sentiment_score)

        #calculating sentiment score using analyzer
        analyzer = SentimentIntensityAnalyzer()
        analyzer_score = analyzer.polarity_scores(tweet.full_text)["compound"]
        analyzer_scores.append(analyzer_score)
    #creating a .csv file
table = {'Tweet':tweets, 'Author':authors, 'Sentiment score':basic_sentiment_scores,'Analyzer sentiment score':analyzer_scores}
df = pd.DataFrame(table)
df.to_csv('Sentiment Analysis of Tweets.csv')

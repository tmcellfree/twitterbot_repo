# Reference adapted from https://www.digitalocean.com/community/tutorials/how-to-create-a-twitterbot-with-python-3-and-the-tweepy-library
# Import Tweepy, sleep, credentials.py
import tweepy
from time import sleep
from datetime import datetime
import csv
import sys
import random   # This is for using random lines in the hashtage list later on
from textblob import TextBlob
import re
datestr = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
################################
#######ADJUST THESE!#############
handle = 'cellfreelab' #this is your twitter handle
dir = '/home/cellfree/twitterbots/'
number_retweets = 2 #this is the number of retweets for each hashtag
#################################
#################################
path = dir+handle+'/'

#Import hashtags (specific to each user) and mastertags (tags that all user retweet)
hashtags=open(dir+'hashtags.txt')
mastertags=open(dir+'mastertags.txt')

# Import credentials file with API keys etc
sys.path.insert(0, path)
import credentials
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Manage followers 
#Refer to http://tweepy.readthedocs.io/en/v3.5.0/api.html#friendship-methods
followers = api.followers_ids("%s" % handle)
friends = api.friends_ids("%s" % handle)

#####################
###Record Keeping####
#####################

#store current followers
store_followers = open(path+'followers/followers_'+datestr+'.txt','w') # 'w' meanscreate file and truncate to zero length
store_followers.writelines(["%s\n" % item  for item in followers])
store_followers.name

#Get the number of followers and store this in a csv for analytics
total_followers = open(path+'/follower_history.csv', 'a') # 'a' means append to file
w=csv.writer(total_followers)
current_followers=len(followers)
fields=[datestr,current_followers]
w.writerow(fields)
#print current_followers

##########################
###Follower Management####
##########################

#Autofollow those that follow you
for s in followers:
    try:
        if s not in friends:
            api.create_friendship(s)
	    print ('Followed  @' + api.get_user(s).screen_name) # Convert User ID to username
	    sleep(5)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
#Purge unreciprocated follows (Warning! This is not good twitter practce so keep number low!)
unfollows = 0
for t in friends:
    f=random.choice(friends) # This prevents unfollowing your most recently followed friend
    if f not in followers:
        if (unfollows < 2): #here is where you select number of unfollows... be careful! You can get banned
            api.destroy_friendship(f)
            print ('Unfollowed  @' + api.get_user(f).screen_name) # Convert User ID to username
            sleep(5)
            unfollows += 1

# For loop to iterate over tweets in hashtag file, limit each with the "number_retweets" variable above
#for line in hashtags:
#Not using this currently   
# INSTEAD
# Enable random choice of hashtag in file
tags = hashtags.read().splitlines()     # Open/Read the file
random_tag =  random.choice(tags)             # Read a random hashtag from a random line
print(random_tag)
tweet_counter = 0  # This counter keeps total retweets fixed
for tweet in tweepy.Cursor(api.search,q=random_tag).items(100):

    try:
   # Print out usernames of the last N (given by variable "number_retweets)" people to use #tag
   # Add \n escape character to print() to organize tweets        
        print('\nTweet by: @' + tweet.user.screen_name)
	######
	##Setiment Analysis ##
	text=tweet.text
        textWords=text.split()
        #print (textWords)
        cleanedTweet=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        print (cleanedTweet)
        #print (TextBlob(cleanedTweet).tags)
        analysis= TextBlob(cleanedTweet)
        #print (analysis.sentiment)        
	if(analysis.sentiment.polarity < 0):
            polarity = 'Negative'
        if (analysis.sentiment.polarity >=0.3) and (analysis.sentiment.subjectivity<=0.8) and (tweet_counter < number_retweets):
            print (analysis.sentiment)
            polarity = 'Positive'
	    tweet_counter = tweet_counter+1	
            print(polarity,tweet_counter)
	#######
        #######
	    # Retweet tweets as they are found
            tweet.retweet()
            print('Retweeted the tweet')
            # Favorite the tweet
            tweet.favorite()
            print('Favorited the tweet')

            # Follow the user who tweeted
            if not tweet.user.following:
                tweet.user.follow()
                print('Followed the user')

            sleep(5)

    #Exception handling, e.g., in case of too many results    
    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break

#MASTERTAGS - All bots retweet these from main directory (twitterbots/mastertags.txt)
# For loop to iterate over tweets in mastertag file, limit each each with the "number_retweets" variable at top of file
for line in mastertags:
    print(line.split('x')[1].split('*')[0])

    for tweet in tweepy.Cursor(api.search,q=line.split('#')[1].split('*')[0]).items(number_retweets):

        try:
            # Print out usernames of the last N (given by the "number_retweets" variable at the top of file) people to use #cellfree
            # Add \n escape character to print() to organize tweets
            print('\nTweet by: @' + tweet.user.screen_name)

            # Retweet tweets as they are found
            tweet.retweet()
            print('Retweeted the tweet')

            # Favorite the tweet
            tweet.favorite()
	    print('Favorited the tweet')

	    # Follow the user who tweeted
            if not tweet.user.following:
                tweet.user.follow()
                print('Followed the user')

            sleep(5)

        #Exception handling, e.g., in case of too many results
        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break


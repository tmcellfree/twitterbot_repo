#!/bin/bash

#Automatically runs the different twitter bots (contained in directories)
#It does this automatically which is the cool thing. 

#If you only want to run specific bots then pick and chose which by uncommenting here
python /home/twitterbots/bot1/retweet_twitterbot.py &
python /home/twitterbots/bot2/retweet_twitterbot.py 

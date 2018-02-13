This is a folder for all the twitterbots used for marketing or promotion
**********************************************************************
python script (retweet_twitterbot.py) adapted from https://www.digitalocean.com/community/tutorials/how-to-create-a-twitterbot-with-python-3-and-the-tweepy-library

***********************************************
***Folder Structure (organisation and subfolders)
************************************************
Each twitter account has a separate folder
Name of folder is the twitter handle (e.g. cellfreelab or tomcellfree)
Within each folder is 
"credentials.py" file that contains the api tokens etc required to access twitter app
"hastags.txt" this is the folder you should consider editing by adding (or removing) relevant hashtags
"retweet_bot.py" is called out and will retweet/like/follow up to 10 accounts/posts for each of the hashtags (from within the last week)

A "mastertag.txt" is contianed in the main directory (twitterbots) 
This is read and reweeted by all bots


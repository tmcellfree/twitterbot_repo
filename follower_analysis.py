########### READ ME ####################################################################
# This script analyses the follower data of all twitter accounts in the subfolders (named as their twitter handle) based on the handles listed in handle.txt
#######################################################################################
import pandas as pd
from datetime import datetime
import numpy as np
import csv
import matplotlib
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.switch_backend('agg')   #This is something copied from stackoverflow on the advice that matplotlib needs to be edited to have some particlar backend renderer
dir = '/home/cellfree/twitterbots/' #This is the directory where this file lives and all other twitterbot related files

color = 0
#########################################
##### Open and extract follower data ####
#########################################
handles = 'handles.txt' # The file containing the twitter handles that you want to analyse NOTE a handy way to produce this file, if you have maintained the directory-handle naming convention, is to use bash command ls -d */ >> handles.txt !! super convenient
f = open(handles, 'r')
handles_length = sum(1 for line in f) #Open and read the length (in Line number) of the file and then close it NOTE for big files this will be memory demanding since you read the entirety of the file, close it and then open it again!! Advice?!
f.close()
handles = open(handles, 'r')
# For each handle you can extract the "follower_history.csv" which has two columns, for number of followers and another for the exact date/time
for line in handles:
    print line.strip() #The ".strip()" is here since line adds a newline "\n"
    path = dir+line.strip()+'/'
    print path
    headers = ['Date','Followers']
    df = pd.read_csv(path+'follower_history.csv')
    print (df)

######################################################################################
# This section calulates the number of followers lost/gained between any two time intervals
# This is done by reading a file "_handle_followers/_date_" which is a record of every follower at the particular timepoint.
#########################################################################################
    #Before entering loop we need to set up some blank arrays
    oldfollowers = []
    followers_lost = []
    followers_gained = []
    #This loop pulls the follower list for each date
    for item in df['Date']:
        date = item
	#print date  #DEBUGGING
	#print  (path+'followers/followers_%s.txt' % date) #DEBUGGING
	newfollowers = np.loadtxt(path+'followers/followers_%s.txt' % date , unpack=True)   
    	if oldfollowers == []: #This is nessecary when starting the loop since array is initially empty
	    oldfollowers = newfollowers
	foll_new = list(set(newfollowers) - set(oldfollowers)) #This gives the difference between the two lists 
	foll_lost = list(set(oldfollowers)-set(newfollowers))
	#print (len(foll_lost)) #DEBUGGING
	followers_lost.append(-abs(len(foll_lost))) #Remember we get the actual names of the followers lost/gained but we want to convert them into raw numbers, hence the len() command NOTE negating this for convenience of visualisation "-abs()"
	#print (len(foll_new)) #DEBUGGING
	followers_gained.append(len(foll_new))
	#print followersondate #DEBUGGING
	#print newfollowers  #DEBUGGING
	oldfollowers = newfollowers # For the sake of the loop remember!
    #Exit Loop

    print "lost followers: %s" % followers_lost
    print "gained followers: %s" % followers_gained

#################################################################
# Extract Dates and follower numbers from "follower_history.csv"
################################################################
    df['Date'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d-%H-%M-%S')) #Basically mapping our dash separated format to the matplotlib readable format
    x = df['Date'] #Our x-axis 
    y = df['Followers'] #Our y-axis
    # Loop to convert total follower number to %increase/decreas in followers
    foll_norm = []
    i = 0
    for item in y:
	if i == 0:
	    i= float(item)
	float_item=float(item)
	foll_norm.append("{0:.2f}".format(100*(float_item-i)/i))    
	#print float_item-i  #DEBUGGING
	i=float(item)
	#print foll_norm    #DEBUGGING
    #Exit Loop

#######################
##### PLOT THE DATA #####
#######################
    #Making the color of plots and iterating 
    cmap = matplotlib.cm.Spectral       # See https://matplotlib.org/examples/color/colormaps_reference.html
    col = cmap(color/float(handles_length))
    color=color+1
    # Plot parameters
    pylab.rcParams['figure.figsize'] = 10, 8  # that's default image size for this interactive session
    #plt.title('Followers') # Preference title
    #USING SUBPLOT to visualise multiple plots on the same chart
    plt.subplot(3, 1, 1)
    plt.plot(x,foll_norm, label='@%s' % line.strip(), color=col) # Follower % change in
    plt.ylabel('% Change Followers', fontsize=13)
    plt.subplot(3, 1, 2)
    plt.bar(range(len(followers_gained)), followers_gained, alpha = 0.1, color=col) # Gained followers
    plt.bar(range(len(followers_lost)), followers_lost, alpha = 0.1, color=col) # Lost followers
    plt.ylabel('Followers Gained/Lost', fontsize=13)
    plt.ylim(-5, 5)
    plt.subplot(3, 1, 3)
    plt.plot(x, y, label='@%s' % line.strip(), color=col) #Raw Followers
    plt.legend(fontsize = 'x-small', loc=2)
    plt.grid(True) #puts dotted lines across chart (handy for analysis)
    #plt.xlim(950,2000) #Preference Add limits on X-Y axis scale
    #plt.ylim(0,4)
    plt.tight_layout(pad=0.4, w_pad=1.0, h_pad=0.5)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()

    #Name and Axes labels
    plt.xlabel('Date/Time', fontsize=13)
    plt.ylabel('Raw Followers', fontsize=13)
    plt.savefig('followers_trend.png')
#####
#END#
#####

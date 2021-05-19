from tkinter import *
from trends import trendsComp
from trends import sendTweet
import tweepy as tw
import pandas as pd

#set up Twitter API
consumer_key= 'ymMXRSBkTYGx1cwmjMXrhpclt'
consumer_secret= 'KxTT7s2mDJRD2qqLZcXotZUUdkIouYagPMg9ViNRYopGkbdtT3'
access_token= '1393947013163716609-VbwLb2w42ECxhhFrQ9OGeisUK1Uv4q'
access_token_secret= 'D3Ut2HC4HgVi3W86XUhccQOdMV8cQkEQt7pL6IxSGiNy9'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#Create City Selection Window
master = Tk()
master.title("Trending Comparison")
#List of cities
options_list = ["Atlanta", "Boston", "Chicago", "Dallas", "New York", "Philadelphia", "San Francisco"]

value_inside = StringVar(master)
value_inside.set("Select an City")

menu = OptionMenu(master, value_inside, *options_list)
menu.pack()

#save off the selected city as a global variable
def saveCity():
    global city
    city = value_inside.get()
    master.destroy()

submit_button = Button(master, text='Submit', command=saveCity)
submit_button.pack()

master.mainloop()
print("City selected: "+city)

#map city to WOEID for Twitter use
worldID = None
if city == "Atlanta":
    worldID = 2357024
elif city == "Boston":
    worldID = 2367105
elif city == "Chicago":
    worldID = 2379574
elif city == "Dallas":
    worldID = 2388929
elif city == "New York":
    worldID = 2459115
elif city == "Philadelphia":
    worldID = 2471217
elif city == "San Francisco":
    worldID = 2487956    
print("World ID: "+str(worldID))
print()

#Call the created function which pulls trends
cityTrends, usTrends, worldTrends = trendsComp(worldID,api)
print("All trends in " + city + ":")
print(cityTrends)
print()

#assign to key value pairs
#if a trend is in the city it is a local trend
#if it is trending in the USA it is a USA trend
#if it is trending in the world it is a world trend
cityDict = dict.fromkeys(cityTrends, "Local Trend")
usDict = dict.fromkeys(usTrends, "USA Trend")
worldDict = dict.fromkeys(worldTrends, "World Trend")

citySet = set(cityDict)
usSet = set(usDict)
worldSet = set(worldDict)

#find intersections with the USA and world trends
for trend in citySet.intersection(usSet):
    #overwrite local trends which are also US trends as US trends in the local dictionary
    cityDict[trend] = usDict[trend]

for trend in citySet.intersection(worldSet):
    #do the same for global overlaps
    cityDict[trend] = worldDict[trend]
print("Trends categorized based on the widest spectrum applicable: ")
print(cityDict)
print()

#If a trend is in the city, in the USA and world then it is a world trend. If it is in city and USA then it is a USA trend. If it's only in the city it is a local trend
#This is what is meant by "widest spectrum"

localTrends = [];
usTrends = [];
worldTrends = [];

#create seperate list for each category
for trend in cityDict:
    if cityDict[trend] == 'Local Trend':
        localTrends += [trend]
    elif cityDict[trend] == 'USA Trend':
        usTrends += [trend]
    elif cityDict[trend] == 'World Trend':
        worldTrends += [trend]

localTopics = ''
usTopics = ''
worldTopics = ''

#organize trends into a string and cap the length once past 150 characters so it is within tweet limits
for topic in localTrends:
    if len(topic)+len(localTopics)>= 150:
        localTopics += topic
        break
    elif topic == localTrends[-1]:
        localTopics += topic
    else:
        localTopics += topic + ', '
        
for topic in usTrends:
    if len(topic)+len(usTopics)>= 150:
        usTopics += topic
        break
    elif topic == usTrends[-1]:
        usTopics += topic
    else:
        usTopics += topic + ', '
        
for topic in worldTrends:
    if len(topic)+len(worldTopics)>= 150:
        worldTopics += topic
        break
    elif topic == worldTrends[-1]:
        usTopics += topic
    else:
        worldTopics += topic + ', '

#create tweet text
localTweet = 'Local Trends for ' + city + ': ' + localTopics
usTweet = 'US Trends: ' + usTopics
worldTweet = 'World Trends: ' + worldTopics

print("Below is the tweet text")
print(localTweet)
print()
print(usTweet)
print()
print(worldTweet)

#send all 3 tweets from created function
sendTweet(localTweet,usTweet,worldTweet,api)

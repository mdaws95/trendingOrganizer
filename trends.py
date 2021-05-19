#function to pull the trends from the selected city as well as USA and World trends
def trendsComp(city,api):    

    #define which woeid to pull trends from then pull them
    woeidCity = city
    trendsCity = api.trends_place(id = woeidCity)

    woeidUSA = 23424977
    trendsUSA = api.trends_place(id = woeidUSA)

    woeidWorld = 1
    trendsWorld = api.trends_place(id = woeidWorld)

    cityTrends = []
    usaTrends = []
    worldTrends = []

    #create list of trends
    for valueCity in trendsCity:
        for trendCity in valueCity['trends']:
            cityTrends += [trendCity['name']]
        
    for valueUSA in trendsUSA:
        for trendUSA in valueUSA['trends']:
            usaTrends += [trendUSA['name']]
            
    for valueWorld in trendsWorld:
        for trendWorld in valueWorld['trends']:
            worldTrends += [trendWorld['name']]

    return cityTrends, usaTrends, worldTrends

#function to send tweets given the tweet text
def sendTweet(local,us,world,api):
    api.update_status(local)
    api.update_status(us)
    api.update_status(world)

import csv
import urllib2
from datetime import date, timedelta
from pymongo import MongoClient

with open('/Users/chris/workspace/geovis_assignments/project/webpages.txt') as webpages:  # List of Andrews stations/webpages
    urls = [x.strip('\n') for x in webpages.readlines()]  # strips the \n

for i in urls:
    station, url = i.split()  # splits the station name and webpage
    try:
        webpage = urllib2.urlopen(url)  # opens the url
        print "Opening webpage for: %s" % station
    except:
        print "Could not open webpage for: %s" % station
    datareader = csv.reader(webpage)  # reads the webpage
    day = date.today() - timedelta(1)  # finds yesterdays date
    yesterday = day.strftime('%Y-%m-%d')  # formats the date
    try:
        mongo_client = MongoClient('mapious.ceoas.oregonstate.edu', 27017)  # opens the mongo db client
        print "Connected Succesfully to MongoDB"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB Atlas: %s" % e

    db = mongo_client.AndrewsMet  # opens the Andrews database

    for each in datareader:
        if each[0] == 'Site':  # gets the key values from the header
            header = (each)
        elif each[1][:10] == yesterday:  # gets yesterdays data
            line = (each)
            data = dict(zip(header, line))  # creates dictionary object
            db[station].insert(data)  # inserts into the right collection
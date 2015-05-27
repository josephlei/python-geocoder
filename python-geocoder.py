
# coding: utf-8

# ####A modified version of Lauren Archer's Simple CSV Geocoder located at https://github.com/laurenarcher/SimpleCsvGeocoder
# 
# ####In this instance, it is used to geocode approximately 620 addresses for the Code for Sacramento WICIT project hosted live at www.findwic.com
# 
# ####Data limitations and notes: The Google Maps Geocoding API allows 2500 address requests per day per IP address or API key, unless you are a Google Work customer.  

# In[1]:

import csv
import time
from pygeocoder import Geocoder


# input_file  = open('API_WIC_SIGNUP_LOCS_TEST.csv', 'rU') #Open your .csv file
# output_file = open('WIC_LOCS_GEO.csv', 'w') #Make an empty .csv This is where your geocodes will end up.
# data        = csv.reader(input_file)        #Read in the raw csv using the csv library's "reader" function
# 
# for line in data:
#     if line[0]!='site': #this excludes the header row, which starts with "site"
#         full_address=line[1]+", "+line[2]+" "+line[3] #build the input string
#         print "Sent to Google:",full_address #Visual confirmation of what was sent to Google's API, remove for minor speed boost
#         results=Geocoder.geocode(full_address) #Dump the returned object into "results" var
#         time.sleep(.21) #Google allows 5 geocodes per second for non Google Work customers, this throttles with a 1/100 sec margin
# output_file.close() #Close the output file to ensure all locks are released
# 
# #In this code block, no items are written to output file, this is a dev/test block, NOT PROD

# In[47]:

#this code block for dev/test exploration of data types and formats

#print results.raw
#print type(results.raw)     # i am a list
#print type(results.raw[0])  # i am a dictionary
#print results.raw[0].keys() # [u'geometry', u'address_components', u'place_id', u'formatted_address', u'types']
#print results.raw[0][u'address_components']


# In[45]:

#This code block is the first iteration of production, change to full file for "real" results, currently intakes a 2 row sample

input_file  = open('API_WIC_SIGNUP_LOCS_TEST.csv', 'rU') #Open your .csv file
output_file = open('WIC_LOCS_GEO.csv', 'w') #Make an empty .csv This is where your geocodes will end up.
data        = csv.reader(input_file)        #Read in the raw csv using the csv library "reader" function

for line in data:
    if line[0]!='site': #this excludes the header row, which starts with "site"
        full_address=line[1]+", "+line[2]+" "+line[3] #build the input string
        print "Sent to Google:",full_address #Visual confirmation of what was sent to Google's API, remove for minor speed boost
        results=Geocoder.geocode(full_address) #Dump the returned object into "results" var
        #next 8 lines to build the results objects I want to output to file, concurrently forcing them into a 1 item list
        #This is intended as a brute force solution so initial prod can be completed.  Iteration for elegance forthcoming...
        lat          = [results.coordinates[0]]
        long         = [results.coordinates[1]]
        street_number= [results.street_number]
        street_name  = [results.route]
        city         = [results.city]
        state        = [results.state]
        zip          = [results.postal_code]
        county       = [results.county]
        new_line = [line[0]] + [line[1]] + street_number+street_name+city+state+zip+county+lat+long #build the output
        csv.writer(output_file).writerow(new_line) #write one line to csv file
        time.sleep(.21)#Google allows 5 geocodes per second for non Google Work customers, this throttles with a 1/100 sec margin
output_file.close() #Close the output file to ensure all locks are released


# #original code from https://github.com/laurenarcher/SimpleCsvGeocoder
# 
# def csvGeocoder(data):
#     for line in data:
#         [siteid,sitename,address,city,zip,phone] = line #Make sure the number of columns matches/aligns with the number of fields listed here.
#         if city == "city": #This skips the header. Don't geocode the header :D
#             Latitude = ["Latitude"]
#             Longitude = ["Longitude"] 
#             new_line = line + Latitude + Longitude #This adds two new columns to your .csv, Latitude and Longitude.
#             csv.writer(output_file).writerow(new_line)
#             print new_line # This isn't required. I just like to watch.
#         else:
#             #I use a column with the Full Address (Street Number, Street, City, Provice/State, Country) But you could concatenate from multiple fields too.
#             results = Geocoder.geocode(address+city+zip)
#             Latitude = [results[0].coordinates[0]] 
#             Longitude = [results[0].coordinates[1]]
#             new_line = line + Latitude + Longitude
#             csv.writer(output_file).writerow(new_line)
#             time.sleep(.25) #This throttles your requests. The GoogleAPI doesn't like too many requests per second.
#             print new_line #Printing to the console makes the process a lot longer. Omit for speed.
#     
#     #del url,City,Address,Ward,Status,ListDate,IntentionDate,ByLaw,PartIVDate,PartVDate,HeritageDistrict,DistrictStatus,HeritageEasement,RegistrationDate,BuildingType,ArchitectBuilder,ConstructionYear,Province,Country,FullAddress,Details,DemoDate,PrimaryAddress, line
#     #del data
# 
#     input_file.close()
#     output_file.close()

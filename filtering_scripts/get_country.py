from geopy.geocoders import Nominatim
import pandas as pd
from geopy.exc import GeocoderTimedOut
import csv

#city_list = pd.read_excel('D:/Semester2/NLP/Project/city_list.xlsx')
business_list = pd.read_csv('D:/Semester2/NLP/Project/filtering_based_on_country/yelp_business_filter_last.csv')

with open('D:/Semester2/NLP/Project/country_list/city_list_country.csv','wb') as csv_file:
    fieldnames = ["business_id","name","neighborhood","address","city","state","postal_code","latitude","longitude","stars","review_count","is_open","categories","Country"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    geolocator = Nominatim()
    for index,row in business_list.iterrows():
        row_hash = {}
        count = 0
        for column in row:
            row_hash[fieldnames[count]] = column
            count+=1
        coordinates = str(row['latitude']) + "," + str(row['longitude'])
        try:
            location = geolocator.reverse(coordinates,timeout=15)
            row_hash['Country'] = location.raw['address']['country']
            if (index % 50 ==0):
                print("Completed --")
                print(index)
        except Exception, e:
            row_hash['Country'] = "NA" + str(e)
        writer.writerow(row_hash)

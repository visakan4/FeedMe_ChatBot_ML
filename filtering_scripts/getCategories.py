import pandas as pd
from collections import Counter
import operator
import json

def get_unique_categories(categories):
    categories_final_list = []
    for category in categories:
        category_list_array = category.split(';')
        for category_element in category_list_array:
            lowerCasedElement = category_element.lower()
            if lowerCasedElement not in categories_final_list:
                categories_final_list.append(lowerCasedElement)
    return Counter(categories_final_list)

def get_categories_count(categories,category_hash):
    for category in categories:
        category_list_array = category.split(';')
        for category_element in category_list_array:
            lowerCasedElement = category_element.lower()
            category_hash[lowerCasedElement]+=1
    return category_hash

def resetCounter(category_details):
    for category in category_details:
        category_details[category] = 0
    return category_details


#Reading yelp business file
business_data = pd.read_csv("yelp_business.csv")
category_details = get_unique_categories(business_data['categories'])
category_count_details = get_categories_count(business_data['categories'],resetCounter(category_details))
sorted_category_count_details = sorted(category_count_details.items(),key=operator.itemgetter(1),reverse=True)
feature_json_value = open('category_data.txt','w')
feature_values_json = json.dumps(sorted_category_count_details)
feature_json_value.write(feature_values_json)
feature_json_value.close()

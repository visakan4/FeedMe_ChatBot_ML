# import json
# from nltk.corpus import stopwords
#
# for id in stopwords.fileids():
#     print(id)

import csv
import codecs

reviews_file = codecs.open("eggs.csv", "wb",encoding='utf-8')
spamwriter = csv.writer(reviews_file)
spamwriter.writerow(["got", "minute", "terrible", "another", "know", "ramen", "food", "u", "waitress", "taste", "noodle"])
spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

# a = []
#
# if not a:
#     print("hello")
# reviews = "ok-ramen"
#
# for index, word in enumerate(words):
#     if word in reviews:
#         print(word)

# def load_json():
#     with open('category_words.txt') as json_data:
#         category_words = json.load(json_data)
#     return set(category_words['ambience']), set(category_words['discount']), set(category_words['food']), set(category_words['service'])
#
#
# ambience_set, discount_set, food_set, service_set = load_json()
# words_set = set(words)
#
# print(food_set.intersection(words_set))
# print(service_set.intersection(words_set))
# print(discount_set.intersection(words_set))
# print(ambience_set.intersection(words_set))
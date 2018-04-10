# encoding=utf8
import pandas as pd
import operator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def detectlanuage(words):
    language_hash = {}
    for id in stopwords.fileids():
        language_stopwords = set(stopwords.words(id))
        wordCount = 0
        for word in words:
            if (word in language_stopwords):
                wordCount+=1
        language_hash[id] = wordCount
    return max(language_hash.iteritems(),key=operator.itemgetter(1))[0]


def main():
    for index, row in review_data.iterrows():
        try:
            words = word_tokenize(row['TEXT'])
            language = detectlanuage(words)
            if (language == 'english'):
                english_writer.writerow(row)
            else:
                other_writer.writerow(row)
        except Exception as e:
            print(e)
            exception_reviews.writerow([index,"NA",str(e)])


review_data = pd.read_csv('review3.csv',encoding='latin-1')
english_reviews = codecs.open("english_reviews.csv","wb",encoding = 'utf-8')
other_reviews = codecs.open("other_reviews.csv","wb",encoding = 'utf-8')
exception_reviews = codecs.open("exception_reviews.csv","wb",encoding = 'utf-8')
english_writer = csv.writer(english_reviews)
other_writer = csv.writer(other_reviews)
exception_reviews = csv.writer(exception_reviews)

main()
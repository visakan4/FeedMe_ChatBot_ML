from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
import codecs
import string
import json
import sys
import csv
reload(sys)
sys.setdefaultencoding('utf8')

file_number = 12

business_data = pd.read_csv('D:/Semester2/NLP/Project/split_business_data_2000/business_data_'+str(file_number)+'.csv')
reviews = pd.read_csv('D:/Semester2/NLP/Project/final_data/english_reviews.csv')
tokenizer = RegexpTokenizer(r'\w+')
lemma = WordNetLemmatizer()
stemmer = PorterStemmer()
sid = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))
business_id_list = list(business_data['business_id'])
complete_data = []


def getPositiveNegativeScoreUsingContains(text):
    sentences = sent_tokenize(text)
    positiveCount = 0
    negativeCount = 0
    for sent in sentences:
        for p in positives:
            if sent.find(p)!=-1:
                positiveCount = positiveCount+1
        for n in negatives:
            if sent.find(n)!=-1:
                negativeCount = negativeCount+1
    return positiveCount,negativeCount


def readFile(relpath):
    with open(relpath,'r') as file:
        lines = file.readlines()
        transitionTable = string.maketrans(string.punctuation, ' '*len(string.punctuation))
        file.close()
        processedLines =[]
        for line in lines:
            line = line.rstrip()
            line = ''.join(line.translate(transitionTable))
            processedLines.append(line)
        return processedLines

positives =set(readFile(r'positive.txt'))
negatives =set(readFile(r'negative.txt'))

def get_text_blob_sentiment(text):
    text = text.decode('utf-8')
    blob_data = TextBlob(text)
    polarity_list = []
    for sentence in blob_data.sentences:
        polarity_list.append(sentence.sentiment.polarity)
    return polarity_list,sum(polarity_list)/len(polarity_list)


def get_sentences(text):
    return sent_tokenize(text.decode('utf-8'))


def get_words(text):
    return tokenizer.tokenize(text.decode('utf-8'))


def get_stop_word_removed_list(review_words):
    stop_word_removed_list = []
    for word in review_words:
        word = word.lower()
        if word not in stop_words:
            stop_word_removed_list.append(word)
    return stop_word_removed_list


def get_lemmatized_words(list_of_words):
    lemmatized_word_list = []
    for word in list_of_words:
        lemmatized_word_list.append(lemma.lemmatize(word.decode('UTF-8')))
    return lemmatized_word_list


def get_stemmed_words(list_of_words):
    stemmed_word_list = []
    for word in list_of_words:
        stemmed_word_list.append(stemmer.stem(word.decode('UTF-8')))
    return stemmed_word_list


def get_overall_score(list_of_reviews,hashKey):
    score_list = []
    for review in list_of_reviews:
        score_list.append(review[hashKey])
    return score_list, sum(score_list)/len(score_list)


def get_calculated_start_value(polariy_score, compound_score):
    star_hash = {}
    if (polariy_score and compound_score == -2) or (polariy_score and compound_score == -3):
        star_hash['polarity_star_value'] = -1
        star_hash['compound_star_value'] = -1
        star_hash['averaged_star_value'] = -1
    else:
        old_min = -1
        old_max = 1
        new_min = 1
        new_max = 5
        polarity_based_star_value = (((polariy_score - old_min) * (new_max - new_min))/(old_max - old_min)) + new_min
        compound_based_star_value = (((compound_score - old_min) * (new_max - new_min))/(old_max - old_min)) + new_min
        averaged_star_value = (polarity_based_star_value + compound_based_star_value)/2
        star_hash['polarity_star_value'] = polarity_based_star_value
        star_hash['compound_star_value'] = compound_based_star_value
        star_hash['averaged_star_value'] = averaged_star_value
    return star_hash


def get_nltk_compound(sentences):
    nltk_polarity = []
    for sentence in sentences:
        ss = sid.polarity_scores(sentence)
        nltk_polarity.append(ss['compound'])
    return nltk_polarity, sum(nltk_polarity) / len(nltk_polarity)


def get_reviews_list(filtered_reviews):
    review_list = []
    for review in filtered_reviews.iterrows():
        review_hash = {}
        review_hash['review_id'] = review[1]['review_id']
        review_hash['complete_text'] = review[1]['text']
        review_hash['review_sentences'] = get_sentences(review[1]['text'])
        review_hash['review_words'] = get_words(review[1]['text'])
        review_hash['stop_word_removed'] = get_stop_word_removed_list(review_hash['review_words'])
        review_hash['stemmed_words'] = get_stemmed_words(review_hash['stop_word_removed'])
        review_hash['lemmatized_words'] = get_lemmatized_words(review_hash['stop_word_removed'])
        review_hash['stars'] = review[1]['stars']
        review_hash['text_blob_polarity_list'], review_hash['text_blob_polarity'] = get_text_blob_sentiment(review[1]['text'])
        review_hash['nltk_compound_list'],review_hash['nltk_compund'] = get_nltk_compound(review_hash['review_sentences'])
        review_hash['positive_word_count'],review_hash['negative_word_count'] = getPositiveNegativeScoreUsingContains(review_hash['complete_text'])
        review_list.append(review_hash)
    return review_list


def get_features():
    for index,business_id in enumerate(business_id_list):
        print(index)
        business_data = {}
        business_data['business_id'] = business_id
        try:
            if not (((reviews[reviews['business_id'].str.contains(business_id)])).empty):
                business_data['reviews_data'] = get_reviews_list(reviews[reviews['business_id'].str.contains(business_id)])
                business_data['reviews_polarity_list'], business_data['overall_polarity_score'] = get_overall_score(business_data['reviews_data'],"text_blob_polarity")
                business_data['reviews_compound_list'], business_data['overall_compound_score'] = get_overall_score(business_data['reviews_data'], "nltk_compund")
                business_data['stars'] = get_calculated_start_value(business_data['overall_polarity_score'],business_data['overall_compound_score'])
            else:
                business_data['reviews_polarity_list'], business_data['overall_polarity_score'] = [],-2
                business_data['reviews_compound_list'], business_data['overall_compound_score'] = [],-2
                business_data['stars'] = get_calculated_start_value(business_data['overall_polarity_score'],business_data['overall_compound_score'])
            complete_data.append(business_data)
        except Exception,e:
            print(str(e))
            business_data['overall_polarity_score'] = -3
            business_data['overall_compound_score'] = -3
            business_data['stars'] = get_calculated_start_value(business_data['overall_polarity_score'],business_data['overall_compound_score'])
            complete_data.append(business_data)


def write_to_file():
    feature_file = codecs.open("business_feature_data_"+str(file_number)+".csv", "wb", encoding='utf-8')
    headers = ["business_id","overall_polarity_score","overall_compound_score","polartiy_star_value","compound_star_value","averaged_star_value"]
    feature_writer = csv.DictWriter(feature_file,fieldnames=headers)
    feature_writer.writeheader()
    for data in complete_data:
        write_hash = {}
        write_hash['business_id'] = data['business_id']
        write_hash['overall_polarity_score'] = data['overall_polarity_score']
        write_hash['overall_compound_score'] = data['overall_compound_score']
        write_hash['polartiy_star_value'] = data['stars']['polarity_star_value']
        write_hash['compound_star_value'] = data['stars']['compound_star_value']
        write_hash['averaged_star_value'] = data['stars']['averaged_star_value']
        feature_writer.writerow(write_hash)


get_features()
write_to_file()
# feature_json_value = open('features_json_'+str(file_number)+'.txt','w')
# feature_values_json = json.dumps(complete_data)
# feature_json_value.write(feature_values_json)
# feature_json_value.close()

# print(json.dumps(complete_data))

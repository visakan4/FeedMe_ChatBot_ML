from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from textblob import TextBlob
import gensim
from gensim import corpora
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

file_number = 1

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
        new_min = 0
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


def get_lda_input(reviews):
    lda_input = []
    for review in reviews:
        lda_input.append(review['stop_word_removed'])
    return lda_input


def get_lda_words(topics):
    words = []
    for topic in topics:
        topics_with_probability = (str(topic[1]).split("+"))
        for word in topics_with_probability:
            prob_list = word.split("*")
            prob_list[1] = prob_list[1].lower().replace('"', ' ').strip()
            if prob_list[1] not in words:
                if prob_list[1].isdigit()!=True:
                    words.append(prob_list[1])
    return (words)


def generate_doc_term_matrix(list_of_words):
    term_dictionary = corpora.Dictionary(list_of_words)
    doc_term_matrix = [term_dictionary.doc2bow(doc) for doc in list_of_words]
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word=term_dictionary, passes=50)
    return ldamodel


def lda_modelling(reviews):
    list_of_words = get_lda_input(reviews)
    ldamodel = generate_doc_term_matrix(list_of_words)
    lda_words = get_lda_words(ldamodel.show_topics(num_topics=3, num_words=5))
    return lda_words


def get_polarity_score(review_data, lda_aspect_set, input_set):
    intersected_words = list(lda_aspect_set.intersection(input_set))
    lda_polarity_score = 0
    lda_compound_score = 0
    for intersected_word in intersected_words:
        text_blob_score_list = []
        compound_score_list = []
        for review in review_data:
            for index, sentence in enumerate(review['review_sentences']):
                if intersected_word in sentence.lower():
                    if review['text_blob_polarity_list'][index]!=0 and review['nltk_compound_list'][index]!=0:
                        text_blob_score_list.append(review['text_blob_polarity_list'][index])
                        compound_score_list.append(review['nltk_compound_list'][index])
        if text_blob_score_list:
            lda_polarity_score += sum(text_blob_score_list)/len(text_blob_score_list)
        if compound_score_list:
            lda_compound_score += sum(compound_score_list)/len(compound_score_list)
    if lda_polarity_score == 0:
        return -2,-2
    else:
        return lda_polarity_score/len(intersected_words),lda_compound_score/len(intersected_words)


def get_features():
    for index,business_id in enumerate(business_id_list):
        print(index)
        business_data = {}
        business_data['business_id'] = business_id
        try:
            if not (((reviews[reviews['business_id'].str.contains(business_id)])).empty):
                business_data['reviews_data'] = get_reviews_list(reviews[reviews['business_id'].str.contains(business_id)])
                business_data['lda_aspects'] = lda_modelling(business_data['reviews_data'])
                business_data['food_polarity_score'],business_data['food_compound_score'] = get_polarity_score(business_data['reviews_data'],set(business_data['lda_aspects']),food_set)
                business_data['service_polarity_score'],business_data['service_compound_score'] = get_polarity_score(business_data['reviews_data'],set(business_data['lda_aspects']),service_set)
                business_data['ambience_polarity_score'],business_data['ambience_compound_score'] = get_polarity_score(business_data['reviews_data'],set(business_data['lda_aspects']),ambience_set)
                business_data['discount_polarity_score'],business_data['discount_compound_score'] = get_polarity_score(business_data['reviews_data'],set(business_data['lda_aspects']),discount_set)
            else:
                business_data['food_polarity_score'], business_data['food_compound_score'] = -4.-4
                business_data['service_polarity_score'], business_data['service_compound_score'] = -4, -4
                business_data['ambience_polarity_score'], business_data['ambience_compound_score'] = -4, -4
                business_data['discount_polarity_score'], business_data['discount_compound_score'] = -4, -4
            complete_data.append(business_data)
        except Exception:
            business_data['reviews_data'] = []
            business_data['food_polarity_score'], business_data['food_compound_score'] = -3,-3
            business_data['service_polarity_score'], business_data['service_compound_score'] = -3,-3
            business_data['ambience_polarity_score'], business_data['ambience_compound_score'] = -3,-3
            business_data['discount_polarity_score'], business_data['discount_compound_score'] = -3,-3
            complete_data.append(business_data)


def write_to_file():
    feature_file = codecs.open("D:/Semester2/NLP/Project/lda_output/lda_business_feature_data_" + str(file_number) + ".csv", "wb", encoding='utf-8')
    headers = ["business_id","food_polarity_score","food_compound_score","service_polarity_score","service_compound_score","ambience_polarity_score","ambience_compound_score","discount_polarity_score","discount_compound_score"]
    feature_writer = csv.DictWriter(feature_file,fieldnames=headers)
    feature_writer.writeheader()
    for data in complete_data:
        write_hash = {}
        write_hash['business_id'] = data['business_id']
        write_hash['food_polarity_score'] = data['food_polarity_score']
        write_hash['food_compound_score'] = data['food_compound_score']
        write_hash['service_polarity_score'] = data['service_polarity_score']
        write_hash['service_compound_score'] = data['service_compound_score']
        write_hash['ambience_polarity_score'] = data['ambience_polarity_score']
        write_hash['ambience_compound_score'] = data['ambience_compound_score']
        write_hash['discount_polarity_score'] = data['discount_polarity_score']
        write_hash['discount_compound_score'] = data['discount_compound_score']
        feature_writer.writerow(write_hash)


def write_reviews_file():
    reviews_file = codecs.open("D:/Semester2/NLP/Project/reviews_output/reviews_sentiment_" + str(file_number) + ".csv", "wb",encoding='utf-8')
    review_file_writer = csv.writer(reviews_file)
    for data in complete_data:
        review_print_data = data['reviews_data']
        for review in review_print_data:
            if review:
                data_to_be_stored = []
                data_to_be_stored.append(data['business_id'])
                data_to_be_stored.append(review['review_id'])
                for index,sentence in enumerate(review['review_sentences']):
                    data_to_be_stored.append(sentence)
                    data_to_be_stored.append(review['text_blob_polarity_list'][index])
                    data_to_be_stored.append(review['nltk_compound_list'][index])
                review_file_writer.writerow(data_to_be_stored)


def load_json():
    with open('category_words.txt') as json_data:
        category_words = json.load(json_data)
    return set(category_words['ambience']), set(category_words['discount']), set(category_words['food']), set(category_words['service'])


ambience_set, discount_set, food_set, service_set = load_json()
get_features()
write_to_file()
write_reviews_file()
# feature_json_value = open('features_json_lda.txt','w')
# feature_values_json = json.dumps(complete_data)
# feature_json_value.write(feature_values_json)
# feature_json_value.close()



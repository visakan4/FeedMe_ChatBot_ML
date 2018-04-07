import pandas as pd

# Replace the file path with your own path
for i, chunk in enumerate(pd.read_csv('D:/Semester2/NLP/Project/review/yelp_review.csv',chunksize=100000)):
    chunk.to_csv('D:/Semester2/NLP/Project/review/review{}.csv'.format(i), index=False)
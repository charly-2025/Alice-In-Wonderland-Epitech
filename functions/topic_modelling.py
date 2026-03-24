from collections import Counter
import nltk
from nltk.corpus import stopwords

def topic_modelling(texte):
    stop_words = set(stopwords.words('english'))
    chapters = texte.split("\r\n\r\n")
    topics = {}
    count = 1
    for i in chapters:
        if len(i) > 600:
            tokens = nltk.word_tokenize(i.lower())
            tokens = [word for word in tokens if word not in stop_words]

            #frequency of each tokens
            frequency = Counter(tokens)
            top_words = [word for word, _ in frequency.most_common(10)]

            if top_words != []:
                topics[count] = top_words
            count += 1
    return topics
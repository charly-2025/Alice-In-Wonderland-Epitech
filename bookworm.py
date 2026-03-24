import pandas as pd
import argparse
import requests
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
import string
import spacy
import locationtagger
import json


# functions imports 

from book_summarizer import book_summarizer
from topic_modelling import topic_modelling

from lexical_diversity_measurements import lexical_diversity_measurements
from named_entities_recognition import named_entities_recognition
from books_similarity import books_similarity


# nltk downloads 
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
translator = str.maketrans('', '', string.punctuation)


# spacy downloads
nlp = spacy.load("en_core_web_sm")


# parser arguments
parser = argparse.ArgumentParser()
parser.add_argument('--info',type=int, help='Select a book with his ID')
parser.add_argument('--download',type=int, help='Select a book with his ID')
parser.add_argument('--clean',type=str, help='Enter a str to clean')
parser.add_argument('--lower',action="store_true", help='Enable lower case')
parser.add_argument('--tokenize',type=str, help='Enter a str to tokenize')
parser.add_argument('--sent',action="store_true", help='Enable split sentences')
parser.add_argument('--stop',action="store_true", help='Enable stopword removing')
parser.add_argument('--punct',action="store_true", help='Enable punctuation removing')
parser.add_argument('--postag',type=str, help='Enter a str to postag')
parser.add_argument("--topics", type=int)
parser.add_argument("--summarize", type=int, help="Enter an id to select a specific book to get the summary of the specific book")
parser.add_argument('--normalize',type=str, help='Enter a str to normalize')
parser.add_argument('--lexdiv',type=int, help='Select a book with his ID')
parser.add_argument('--entities',type=int, help='Select a book with his ID')
parser.add_argument('--similar',type=int, help='Select a book with his ID')
parser.add_argument('--noauthor',action="store_true", help='remove book with the same autor')
args = parser.parse_args()


# df reading the catalog
df = pd.read_csv("pg_catalog.csv")

# commun functions

def split_into_sentences(text):
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s*'
    sentences = re.split(pattern, text)
    return [s.strip() for s in sentences if s.strip()]

    return [s.strip() for s in sentences if s.strip()]

def tokenize(text):
    text = ' '.join(word.strip(string.punctuation) for word in text )
    if text.find("***") != -1 :
        text = text.split('***', 2)[2]
    text = text.replace("[Illustration]","")
    text = " ".join(text.split())
    stop_words = set(stopwords.words('english')) 
    tokens = nltk.word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def clean_book(text):
    tail, sep, text = text.partition('*** START OF THE PROJECT GUTENBERG EBOOK')
    text, sep, tail = text.partition('*** END OF THE PROJECT GUTENBERG EBOOK')
    text = re.sub(r'[^a-zA-Z0-9\s\n]', '', text)
    return text

def get_book_by_url(ID):
    book = requests.get(f"https://www.gutenberg.org/cache/epub/{ID}/pg{ID}.txt").text
    return book

# Project

# Lexical diversity measurments
lexdiv = args.lexdiv
if lexdiv :
    try :
        book = get_book_by_url(lexdiv)
        book = clean_book(book)
        print(lexical_diversity_measurements(book))
    except :
        raise ValueError


# Named Entities Recognition

entities = args.entities
if entities :
    try :
        book = get_book_by_url(entities)
        book = clean_book(book)
        print(named_entities_recognition(book))
    except :
        raise ValueError


# Books similarity

similar = args.similar
noauthor = args.noauthor
if similar :
    try :
        print(books_similarity(df,similar,noauthor))
    except :
        raise ValueError


# Topic modeling

if args.topics:
    try:
        texte = requests.get(f"https://www.gutenberg.org/cache/epub/{args.topics}/pg{args.topics}.txt").text
        tail, sep, texte = texte.partition('*** START OF THE PROJECT GUTENBERG EBOOK')
        texte, sep, tail = texte.partition('*** END OF THE PROJECT GUTENBERG EBOOK')
        texte = re.sub(r'[^a-zA-Z0-9\s\n]', '', texte)
        print(topic_modelling(texte))
    except:
        raise ValueError

# Book summarization
    
if args.summarize:
    try:
        texte = requests.get(f"https://www.gutenberg.org/cache/epub/{args.summarize}/pg{args.summarize}.txt").text
        tail, sep, texte = texte.partition('*** START OF THE PROJECT GUTENBERG EBOOK')
        texte, sep, tail = texte.partition('*** END OF THE PROJECT GUTENBERG EBOOK')
        texte = re.sub(r'[^a-zA-Z0-9\s\n]', '', texte.lower())
        summary = book_summarizer(texte, 2)
        for sentence in summary:
            print(sentence)
    except:
        raise ValueError

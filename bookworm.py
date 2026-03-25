import pandas as pd
import argparse
import requests
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import spacy
import csv
from pprint import pprint
import wget

# functions imports 

from functions.book_summarizer import book_summarizer
from functions.topic_modelling import topic_modelling
from functions.lexical_diversity_measurements import lexical_diversity_measurements
from functions.named_entities_recognition import named_entities_recognition
from functions.books_similarity import books_similarity


# nltk downloads 
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
translator = str.maketrans('', '', string.punctuation)


# spacy downloads
nlp = spacy.load("en_core_web_sm") # python -m spacy download en_core_web_sm


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
parser.add_argument('--card',type=int, help='retrieve informations from a book')
parser.add_argument('--cover',action="store_true", help='download the book cover')
parser.add_argument('--book_cat',type=str, help='retrieve information and download all books from a specific category')
args = parser.parse_args()


# df reading the catalog
df = pd.read_csv("requirements/pg_catalog.csv")

# commun functions

def split_into_sentences(text):
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s*'
    sentences = re.split(pattern, text)
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

def dl_book_cover(ID,title):

        image_url = f"https://www.gutenberg.org/cache/epub/{ID}/images/cover.jpg"
        filename = f"cover/{title}-cover.jpg"

        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded as {filename}")
        else:
            print("Failed to download image")


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
        texte = get_book_by_url(args.topics)
        texte = clean_book(texte)
        print(topic_modelling(texte))
    except:
        raise ValueError

# Book summarization
    
if args.summarize:
    try:
        texte = get_book_by_url(args.topics)
        texte = clean_book(texte)
        summary = book_summarizer(texte, 2)
        for sentence in summary:
            print(sentence)
    except:
        raise ValueError


# Book Card

if args.card:
    try:
        book = get_book_by_url(args.card)
        book = clean_book(book)
        with open('requirements/pg_catalog.csv') as csvfile:
            f = csv.reader(csvfile)
            for row in f:
                if row[0] == str(int(args.card)):
                    infos = {"id" : row[0], "type": row[1], "date": row[2], "title": row[3], "author": row[5], "language": row[4], "bookshelves": row[6]}
        book_card = {
            "info": infos,
            "lexdiv" : lexical_diversity_measurements(book),
            "topics": topic_modelling(book),
            "entities": named_entities_recognition(book),
            "summary": book_summarizer(book),
            "similar": books_similarity(df,args.card,noauthor)
        }
        
        if args.cover :
            dl_book_cover(args.card,infos["title"])

        pprint(book_card)
    except:
        raise ValueError


def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

if args.book_cat:
    with open('requirements/pg_catalog.csv') as csvfile:
        f = csv.reader(csvfile)
        for row in f:
            if contains_word(row[8], args.book_cat) == True:
                infos = {"id" : row[0], "type": row[1], "date": row[2], "title": row[3], "author": row[5], "language": row[4], "bookshelves": row[6]}
                book = get_book_by_url(row[0])
                book = clean_book(book)
                book_card = {
                    "info": infos,
                    "lexdiv" : lexical_diversity_measurements(book),
                    "topics": topic_modelling(book),
                    "entities": named_entities_recognition(book),
                    "summary": book_summarizer(book),
                    "similar": books_similarity(df,int(row[0]),noauthor)
                }
                pprint(book_card)
                wget.download(f"https://www.gutenberg.org/cache/epub/{row[0]}/pg{row[0]}.txt")
                
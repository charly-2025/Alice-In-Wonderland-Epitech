import pandas as pd
import argparse
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
import string

stop_words = set(stopwords.words('english'))
translator = str.maketrans('', '', string.punctuation)


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

parser.add_argument('--normalize',type=str, help='Enter a str to normalize')

args = parser.parse_args()

df = pd.read_csv("pg_catalog.csv")


def split_into_sentences(text):
    pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s*'
    sentences = re.split(pattern, text)
    return [s.strip() for s in sentences if s.strip()]


if args.info :
    result = list(df.loc[df["Text#"]==args.info,["Title","Authors","Bookshelves"]].values)[0]
    dic = {
        "id":args.info,
        "title":result[0],
        "authors":result[1],
        "bookshelves":result[2]
    }
    print(dic)


if args.download:
    url = "https://www.gutenberg.org/cache/epub/"+str(args.download)+"/pg"+str(args.download)+".txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open("pg"+str(args.download)+".txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


if args.clean :
    text = args.clean
    if text.find("***") != -1 :
        text = text.split('***', 2)[2]
    clean = text.replace("[Illustration]","")
    clean = " ".join(clean.split())
    if args.lower :
        print(clean.lower())
    else :
        print(clean)




if args.tokenize :
    
    text = args.tokenize
    if text.find("***") != -1 :
        text = text.split('***', 2)[2]
    text = text.replace("[Illustration]","")
    text = " ".join(text.split())

    if args.sent :
        text = split_into_sentences(text)
    else : 
        text = re.findall(r"[\w']+|[.,!?;]",text)

    if args.punct :
        text = [word.translate(translator) for word in text if word]
    
    if args.stop:
        text = [word for word in text if word not in stop_words]

    text = [word for word in text if word != ""]

    print(text) 
    
if args.postag :
    tokens = nltk.word_tokenize(args.postag)
    pos_tags = nltk.pos_tag(tokens)
    print(pos_tags)

if args.normalize :
    text = args.normalize
    tokens = nltk.word_tokenize(text.lower())

    lancaster = LancasterStemmer()

    print([lancaster.stem(t) for t in tokens ])
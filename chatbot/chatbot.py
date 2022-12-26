import aiml
import pandas as pd
import time
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from flask import Flask, jsonify, request
import nltk
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)


df = pd.read_csv('DataMovies.csv')
# print(df)

def casefolding(teks):
    # print(teks)
    return teks.lower()


def tokenfilter(teks):
    stop_words = set(stopwords.words("indonesian"))
    word_tokens = word_tokenize(teks)
    filtered_text = {word for word in word_tokens if word not in stop_words}
    return filtered_text
title = ""
recom = ""
A = {'spy', 'x', 'family','anime'}
B = {'spy', 'family', 'x'}

def overlap(A, B):
    atas = A.intersection(B)
    bawah = min(A, B)
    similarity = len(atas) / len(bawah)
    return similarity

simi = overlap(A, B)
# print(simi)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

time.clock = time.time

kernel = aiml.Kernel()
kernel.learn("AIML.aiml")

# inputan = 'Halo anak Baik membaik sekali la kamu'

# while True:
# @app.route("/bot", methods=["POST"])
@app.route("/bot", methods=["GET"])
def response():
    query = dict(request.args)['query']
    # query = dict(request.args)['query']

    input_text = query
    # input_text = input('User> ')
    input_text = casefolding(input_text)
    start = time.time()
    if 'film dibintangi' in input_text or 'berikan rekomendasi film yang dibintangi' in input_text:
        jawaban = kernel.respond(input_text)
        input_text = stemmer.stem(input_text)
        input_text = tokenfilter(input_text)
        print(jawaban)
        # print(len(df))
        i = 0
        index = []
        for row in df.iterrows():
            if i == len(df):
                break
            star = df.iloc[i]['Actors']
            # print(star)
            star = casefolding(star)
            star = tokenfilter(star)
            star_overlap = overlap(input_text, star)
            print(star_overlap)
            if star_overlap >= 0.3:
                index.append(df.iloc[i]['Title'])      
            i = i + 1
        title_random = random.choices(index, k=3)
        title = ''
        for x in title_random:
            if title == '':
                title = x
            else:
                title = title + ', ' + x
        end = time.time()
        return jsonify( jawaban + ' ' + title)
        # print('Bot> ' + jawaban + ' ' + title)
        # print(end-start)
    elif 'film dengan genre' in input_text or 'berikan rekomendasi film dengan genre' in input_text:
        jawaban = kernel.respond(input_text)
        input_text = stemmer.stem(input_text)
        input_text = tokenfilter(input_text)
        i = 0
        index = []
        for row in df.iterrows():
            if i == len(df):
                break
            genre = df.iloc[i]['Genre']
            genre = casefolding(genre)
            genre = tokenfilter(genre)
            genre_overlap = overlap(input_text, genre)
            print(genre_overlap)
            if genre_overlap >= 0.2:
                index.append(df.iloc[i]['Title'])      
            i = i + 1
        title_random = random.choices(index, k=3)
        title = ''
        for x in title_random:
            if title == '':
                title = x
            else:
                title = title + ', ' + x
        end = time.time()
        return jsonify(  jawaban + ' ' + title)
        # print('Bot> ' +  jawaban + ' ' + title)
        # print(end-start)
    elif 'film yang mirip dengan' in input_text or 'apa saja film yang mirip dengan' in input_text:
        jawaban = kernel.respond(input_text)
        input_text = stemmer.stem(input_text)
        input_text = tokenfilter(input_text)
        i = 0
        index = []
        for row in df.iterrows():
            if i == len(df):
                break
            title = df.iloc[i]['Recom']
            title = casefolding(title)
            title = tokenfilter(title)
            title_overlap = overlap(input_text, title)
            print(title_overlap)
            if title_overlap >= 0.3:
                index.append(df.iloc[i]['Title'])      
            i = i + 1
        title_random = random.choices(index, k=3)
        title = ''
        for x in title_random:
            if title == '':
                title = x
            else:
                title = title + ', ' + x
        end = time.time()
        return jsonify( jawaban + ' ' + title)
        # print('Bot> ' + jawaban + ' ' + title)
        # print(end-start)
    else:
        return jsonify('Maaf saya tidak bisa menjawab pertanyaan tersebut')
        # print('Bot> Maaf saya tidak bisa menjawab pertanyaan tersebut')
    # print(input_text)
    # print(input_text)
    # response = kernel.respond(input_text)
    # print("Bot> " + response)
if __name__ == "__main__":
    app.run(debug=True)

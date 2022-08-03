# from flask import Flask, redirect, render_template, url_for
from flask import Flask, request, render_template, url_for,redirect

app = Flask(__name__)

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer 
# Lemmatize with POS Tag
from nltk.corpus import wordnet
from fuzzywuzzy import fuzz
# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()



def get_wordnet_pos(word):
    # Map POS tag to first character lemmatize() accepts
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


@app.route("/")
def home():
    return render_template("form.html")
    
    
@app.route("/learn",methods=['GET','POST'])
def lear():
    return render_template("index.html")

@app.route('/res', methods=['POST'])
def my_form_post():
    text = request.form['text']
        
    # Init Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize a Sentence with the appropriate POS tag
    sentence = text
    dict_keywords = {"class": 0, "variable": 0, "setup": 0, "object": 0, "function": 0, "comment": 0}

    sentence_list = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)]
    print(sentence_list)

    # for word in sentence_list:
    #     if word in dict_keywords:
    #         dict_keywords[word] = dict_keywords[word] + 1

    for word in sentence_list:
        for key in dict_keywords:
            if fuzz.ratio(word, key) > 80:
                dict_keywords[key] = dict_keywords[key] + 1


    print(dict_keywords)

    words = []
    for key in dict_keywords:
        if dict_keywords[key] > 0:
            words.append(key)

    print(words) 

    return "Your topic request is being processed..."


# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"


if __name__ == "__main__":
    app.run()







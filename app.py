from flask import send_file,   Flask, redirect, render_template, url_for
# from crypt import methods
import logging
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
import nltk
from flask import send_from_directory, Flask, request, render_template, url_for, redirect, jsonify
from firebase_admin import credentials, firestore, initialize_app
import requests


import os.path
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "somesecretkey"
 
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.png']
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]
 
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
# <<<<<<< HEAD
todo_ref = db.collection('todos')
 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# =======
# todo_ref = db.collection('keywords')
# >>>>>>> 84dd66fafd764c527993fc9ae8ebd16abc773985
BASE = "http://127.0.0.1:5000/"
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# Lemmatize with POS Tag
# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()

it = {}

# it =    {'1.Welcome to Python.org':'Python is a popular general-purpose programming language. It is used in machine learning, web development, desktop applications, and many other fields.','Introduction to Python - W3Schools' : '2.Python is a popular programming language. It was created by Guido van Rossum, and released in 1991. It is used for: web development (server-side),',
#         '3.Python Programming Language - GeeksforGeeks':' Python is a high-level, general-purpose and a very popular programming language. Python programming language (latest Python 3) is being used ...',
#         '4.Lists in python' : 'In Python, a list is created by placing elements inside square brackets [] , separated by commas. ... A list can have any number of items and they may be of ...' ,
#         '5. Data Structures — Python 3.10.6 documentation':'List comprehensions provide a concise way to create lists. Common applications are to make new lists where each element is the result of some operations applied ...',
#         '6.Python Lists and List Manipulation | by Michael Galarnykhttps://towardsdatascience.com › python-basics-6-lists-a...':'Each item in a list has an assigned index value. It is important to note that python is a zero indexed based language. All this means is that the first item in ...',
#         '7.Python Programming - Wikibooks, open books for an open world' : 'This book describes Python, an open-source general-purpose interpreted programming language available for the most popular operating systems.', 
#         '8.Complete Python Programming Python Basics to Advanced ...https://www.udemy.com › ... › Python':'10-Aug-2022 — Learn Python programming Python functions Python loops Python files Python DB Python OOP Python regex Python GUI game.',
#         '9.Python 3 Programming Specialization - Courserahttps://www.coursera.org › ... › Software Development':'Offered by University of Michigan. Become a Fluent Python Programmer. Learn the fundamentals and become an independent programmer. Enroll for free.'
#         }


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


@app.route("/learn", methods=['GET', 'POST'])
def lear():
    return render_template("index.html",it = it)


@app.route('/res', methods=['POST'])
def my_form_post():
    text = request.form['text']

    # Init Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize a Sentence with the appropriate POS tag
    sentence = text
    dict_keywords = {"class": 0, "variable": 0, "setup": 0,
                     "object": 0, "function": 0, "comment": 0,"python":0 , "list" : 0,"dictionary": 0, "tuple":0 }

    sentence_list = [lemmatizer.lemmatize(
        w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)]
    print(sentence_list)

    # for word in sentence_list:
    #     if word in dict_keywords:
    #         dict_keywords[word] = dict_keywords[word] + 1

    for word in sentence_list:
        for key in dict_keywords:
            if fuzz.ratio(word, key) > 50:
                dict_keywords[key] = dict_keywords[key] + 1

    print(dict_keywords)

    words = []

    

    list_labels = {
        "list" : "Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are Tuple, Set, and Dictionary, all with different qualities and usage.Python Lists are just like dynamically sized arrays, declared in other languages (vector in C++ and ArrayList in Java). In simple language, a list is a collection of things, enclosed in [ ] and separated by commas.... read more ",
        "python": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming.Dictionaries are used to store data values in key:value pairs. A dictionary is a collection which is ordered*, changeable and do not allow duplicates...... read more",
        "tup" : "xyz"
       }
#  

    for key in dict_keywords:
        if dict_keywords[key] > 0:
            words.append(key)
            it[key] = list_labels[key]
    print(words)


    return redirect("http://127.0.0.1:5000/learn", code=302)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    shepherd = filename
    stt = "{}.txt".format(shepherd)
    logging.info('Downloading file= [%s]', stt)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, stt, as_attachment=True)

# @app.route('/download')
# def download_file():
#     p = "lists.txt"
#     return send_file(p,as_attachment=True)



# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"


if __name__ == "__main__":
    app.run()
# @app.route('/add', methods=['POST'])
# def create():
#     """
#         create() : Add document to Firestore collection with request body
#         Ensure you pass a custom ID as part of json body in post request
#         e.g. json={'id': '1', 'title': 'Write a blog post'}
#     """
#     try:
#         id = request.json['id']
#         todo_ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# @app.route('/list', methods=['GET'])
# def read():
#     """
#         read() : Fetches documents from Firestore collection as JSON
#         todo : Return document that matches query ID
#         all_todos : Return all documents
#     """
#     try:
#         # Check if ID was passed to URL query
#         todo_id = request.args.get('id')
#         if todo_id:
#             todo = todo_ref.document(todo_id).get()
#             return jsonify(todo.to_dict()), 200
#         else:
#             all_todos = [doc.to_dict() for doc in todo_ref.stream()]
#             return jsonify(all_todos), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# @app.route('/callDelete', methods=['GET'])
# def callDelete():
#     return render_template("delete.html")


# @app.route('/deleteByPost', methods=['POST'])
# def deleteByPost():
#     id = request.form.get('id')
#     response = requests.delete(
#         BASE + f"delete?id={id}")
#     response.raise_for_status()  # raises exception when not a 2xx response
#     if response.status_code != 204:
#         return response.json()

#     return False


# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection
#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         todo_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/addByPost', methods=['POST'])
# def addByPost():
#     id = request.form.get('id')
#     title = request.form.get('title')
#     response = requests.post(
#         BASE + "add", json={'id': id, 'title': title})
#     response.raise_for_status()  # raises exception when not a 2xx response
#     if response.status_code != 204:
#         return response.json()

#     return False
# @app.route('/callAdd', methods=['GET'])
# def callAdd():
#     return render_template("add.html")

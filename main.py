#!/usr/bin/env python

import numpy as np
from pathlib import Path
import json
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import random
from nltk.corpus import stopwords

def load_intents(location):
    intents_data = Path(location).read_text()
    return json.loads(intents_data)['intents']

# converts the loaded json data to a pandas table
def load_dataset(data_collection):
    dataset = pd.DataFrame(columns=['intent', 'text'])

    for data in data_collection:
        
        intent = data['intent']
        
        for text in data['text']:
            row = {'intent': intent, 'text': text}
            dataset = dataset.append(row, ignore_index=True)
    
    return dataset

# Vectorize all the texts #

# text to vector
def text_to_vector(text):
    
    # package
    from sklearn.feature_extraction.text import CountVectorizer
    
    # text to vector
    vectorizer = CountVectorizer()
    text_vectors = vectorizer.fit_transform(text)
    txt1_vector = text_vectors.toarray()[0]
    txt2_vector = text_vectors.toarray()[1]
    
    return txt1_vector, txt2_vector


def get_euclidean_distance(txt1, txt2):
    
    # texts combined
    text = [txt1, txt2]
    
    # text to vector
    txt1_vector, txt2_vector = text_to_vector(text)
    
    # return the euclidean distance
    return euclidean_distances([txt1_vector], [txt2_vector])


# Getting the intent of the user #
# iterate through the dataset comparing the text and looking for the closest to the input

def get_intent(text):
    maximum = 5000.0
    intent = ''
    for row in dataset.iterrows():
        dist = get_euclidean_distance( text.lower(), row[1]['text'].lower() )
        if dist < maximum:
            maximum = dist
            intent = row[1]['intent'] 
    return intent

name = ['']     # name capturing
general_context = [('', '')]        # context capturing

def respond(text, intent, data):
    
    # if name is inputted set the global name
    if intent == 'GreetingResponse':
        set_name(text)
    
    text = ''
    
    # amount of sentence flexibility
    random_position = int(random.random() * len(data['responses']))
    text = data['responses'][random_position].replace('<HUMAN>', name[len(name) - 1])
    
    return text


# the dictionary by its intent
def get_data(intent):
    for data in data_collection:
        if data['intent'] == intent:
            return data

# get the name of the user and replace the <HUMAN> in the responses
def set_name(text):
    
    # split the text using spaces
    result = text.split()
    
    # check the 3rd and 4th word for the one thats not a stop word
    result = result[len(result)-1]
    
    name.append(result)
        
# get the response of a text using its intent
def get_response(text):
    
    # the data
    intent = get_intent(text)
    data = get_data(intent)
    
    # get the context of the user text
    context = data['context']
    context_set = (context['out'], context['in'])
    
    main_context = general_context[0]
    result = ''
    
    if main_context == ('', ''):
        main_context = context_set
        result = respond(text, intent, data)
    elif context_set == (main_context[1], main_context[0]):
        result = respond(text, intent, data)
        main_context = ('', '')
    else:
        result = "you haven't answered me yet?"
    
    general_context[0] = main_context
    
    return result

# program starts here

# loading the dataset
data_collection = load_intents("Intent v2.0.json")
dataset = load_dataset(data_collection)

while True:
    text = str(input("Input:"))
    if text.lower() != "exit":
        print("Response:",get_response(text))
    else:
        print("Response: Exiting...")
        break
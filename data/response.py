from data.intent import get_intent
from nltk.corpus import stopwords
import random
from data.chat_database import data_collection

name = ['']

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
    
    # if name is inputted set the global name
    if intent == 'GreetingResponse':
        set_name(text)
    
    
    # amount of sentence flexibility
    random_position = int(random.random() * len(data['responses']))
    text = data['responses'][random_position].replace('<HUMAN>', name[len(name) - 1])
    
    return text
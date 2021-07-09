from data.text_distance import get_euclidean_distance
from data.chat_database import dataset

def get_intent(text):
    maximum = 5000.0
    intent = ''
    for row in dataset.iterrows():
        dist = get_euclidean_distance( text, row[1]['text'] )
        if dist < maximum:
            maximum = dist
            intent = row[1]['intent'] 
    return intent
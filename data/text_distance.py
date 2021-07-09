from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import CountVectorizer


# text to vector
def text_to_vector(text):
    
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
    
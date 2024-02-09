
import pickle
import json

f = open("./datasets/Movies_and_TV/Movies_and_TV_reviews.strict", 'w')
with open('./datasets/Movies_and_TV/Movies_and_TV_reviews.pickle', 'rb') as file:
    data = pickle.load(file)
    for row in data:
        if 'sentence'in row:
            f.write(json.dumps(row))


# from https://github.com/jsvine/markovify

import markovify
import nltk
import re
nltk.download('averaged_perceptron_tagger')


from nltk.tokenize import TweetTokenizer


def build_model(filename):
    
    # Get raw text as string.
    with open(filename) as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text)

    return text_model
    

def noun_finder(sentence):

    tknzr = TweetTokenizer()    
    text = tknzr.tokenize(sentence)

    words = ["::".join(tag) for tag in nltk.pos_tag(text) ]

    pattern = r'(.*)\::NN'
    
    nouns = [w for w in words if 'NN' in w]

    just_words = []
    for w in words:
        match = re.match(pattern, w)
        if match:
            just_words.append(match.group(1))
            

    return just_words


def print_examples(text_model):
    
    # Print five randomly-generated sentences
    for i in range(5):
        print(text_model.make_sentence())


    # Print three randomly-generated sentences of no more than 140 characters
    for i in range(3):
        print(text_model.make_short_sentence(140))



if __name__ == '__main__':

    
    model = build_model("lorem.txt")

    #print_examples(model)
    
    sentence = "Put big game trophy decision on hold until such time as I review all conservation facts. Under study for years. Will update soon with Secretary Zinke. Thank you!"

    print(noun_finder(sentence))

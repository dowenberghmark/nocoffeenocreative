# from https://github.com/jsvine/markovify

import markovify
import nltk
import re
nltk.download('averaged_perceptron_tagger')


from nltk.tokenize import TweetTokenizer


class POSifiedText(markovify.Text):

    # Example from https://github.com/jsvine/markovify
    #def word_split(self, sentence):
    #    words = re.split(self.word_split_pattern, sentence)
    #    words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
    #    return words
#
#    # Example from https://github.com/jsvine/markovify
#    def word_join(self, words):
#        sentence = " ".join(word.split("::")[0] for word in words)
#        return sentence

    def test_sentence_output(self, words, max_overlap_ratio, max_overlap_total):
        """
        Given a generated list of words, accept or reject it.

        Matches with overlap (built-in) and by matching to a list of user-strings (extended).
        """
        l_words = [s.lower() for s in words]
        l_userwords = [s.lower() for s in user_words]

        if set(l_words).intersection(l_userwords):
            return markovify.Text.test_sentence_output(self, words, max_overlap_ratio, max_overlap_total)
        else:
            return False


def build_model(filename):

    # Get raw text as string.
    with open(filename) as f:
        text = f.read()

    # Build the model.
    text_model = POSifiedText(text)

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

    user_words = noun_finder(sentence)

    print_examples(model)
    # print(user_words)

import json
import string
from random import random

import nltk
import rowordnet
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

wn = rowordnet.RoWordNet()
nltk.download('punkt')
stemmer = SnowballStemmer("romanian")
stop_words = []
with open("stopwords-ro.txt", 'r', errors='ignore') as stop_file:
    stop_words = stop_file.read().splitlines()


def to_sentence_list(path):
    """
    Returns list of sentences from a text file
    """
    f = open(path, 'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()  # converts to lowercase
    sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
    return sent_tokens


def remove_punctuation(sent_list):
    """
    Removes punctuations from a list of strings
    """
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    res = [sent.translate(remove_punct_dict) for sent in sent_list]
    return res


def remove_stop_words(sent):
    """
    Removes the stop word in Romanian from a sentence
    """
    sent_list = sent.split(" ")
    res = [x for x in sent_list if x not in stop_words]
    return " ".join(res)


def remove_stop_words_from_list(sent):
    """
    Removes the stop word in Romanian from a sentence list
    """
    res = [remove_stop_words(x) for x in sent]
    return res


def read_json(path):
    """
    Read JSON from file
    """
    f = open(path, 'r', errors='ignore')
    raw = f.read()
    result = json.loads(raw)
    return result


def stemSentence(sentence):
    """
    From a sentence return the list of stemmed words
    """
    token_words = nltk.word_tokenize(sentence)
    stem_sentence = []
    return [stemmer.stem(word) for word in token_words]


def response(user_response, sent_tokens, responses):
    """
    Match the user_response with the list of sentences in sent_tokens using tf-idf, then return the response
    with the same index as the matched sentence
    :param user_response: user input
    :param sent_tokens: list of sentences to be matched
    :param responses: responses corresponding to the sentences
    :return: matched response
    """
    robo_response = ''
    sent_tokens.append(user_response)
    tfidf_vec = TfidfVectorizer(tokenizer=stemSentence)
    tfidf = tfidf_vec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = robo_response + "Scuze, nu inteleg"
        return robo_response
    else:
        robo_response = robo_response + responses[idx]
        return robo_response


def syn_response(user_response, sent_tokens, responses):
    """
    Match the user_response with the list of sentences in sent_tokens using `sentence_similarity`, then return the
    response with the same index as the matched sentence
    :param user_response: user input
    :param sent_tokens: list of sentences to be matched
    :param responses: responses corresponding to the sentences
    :return: matched response
    """
    user_response = remove_stop_words(user_response)
    sent_scores = {idx: sentence_similarity(user_response, val) for idx, val in enumerate(sent_tokens)}
    max_id = max(sent_scores, key=sent_scores.get)
    return responses[max_id]


def greeting(sentence):
    greeting_inputs = ("buna", "salut", "neata", "servus")
    greeting_responses = ["buna", "salut", "neata", "servus", "prezent!"]
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)


def word_similarity(word1, word2):
    """
    Returns the similarity between word1 and word2.
    Returns 1 if the stems are equal and 1/dist**2 if not, where dist is the shortest path between synsets
    corresponding to the words
    :return: similarity between 1,0
    """
    if stemmer.stem(word1) == stemmer.stem(word2):
        return 1
    synsets1 = wn.synsets(literal=word1)
    if not synsets1:
        return 0
    synsets2 = wn.synsets(literal=word2)
    if not synsets2:
        return 0
    try:
        path_length = len(wn.shortest_path(synsets1[0], synsets2[1]))
    except:
        return 0
    return 1/path_length**2


def sentence_similarity(sen1, sen2):
    """
    Computes similarity between the two sentences by applying `word_similarity` for the cartesian product between
    the words from the two sentences
    """
    if not sen1 or not sen2:
        return -1
    score, count = 0.0, 0
    for word1 in nltk.word_tokenize(sen1):
        best_score = max([word_similarity(word1, word2) for word2 in nltk.word_tokenize(sen2)])
        score += best_score
        count += 1
    score /= count
    return score

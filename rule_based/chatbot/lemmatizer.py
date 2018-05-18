import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from fuzzwuzzy import fuzz

def select_noun_verbs_base(sentence, list_only=False):                                                                                                                                                 
    t_sentence = nltk.word_tokenize(sentence)                                                                            
    tags_words = nltk.pos_tag(t_sentence)
    select_words = [(word,tag) for word,tag in tags_words if tag in ('NN','VB')]
    if list_only:
        return [word for word,tag in select_words]
    return select_words

def select_noun_verbs(sentence, list_only=False):                                                                                                                                                      
    t_sentence = nltk.word_tokenize(sentence)                                                                            
    tags_words = nltk.pos_tag(t_sentence)
    select_words = [(word,tag) for word,tag in tags_words if tag.startswith('NN') or 
        tag.startswith('VB')]
    if list_only:
        return [word for word,tag in select_words]
    return select_words

def lemmatize_word(word):
    lemma = WordNetLemmatizer()
    return lemma.lemmatize(word)

def fuzzymatcher(question, query, partial=False):
    if partial:
        return fuzz.partial_ratio(question, query)
    return fuzz.ratio(question, query)

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

def select_noun_verbs_base(sentence):                                                                                                                                                 
    t_sentence = nltk.word_tokenize(sentence)                                                                            
    tags_words = nltk.pos_tag(t_sentence)
    select_words = [(word,tag) for word,tag in tags_words if tag in ('NN','VB')]
    return select_words

def select_noun_verbs(sentence):                                                                                                                                                      
    t_sentence = nltk.word_tokenize(sentence)                                                                            
    tags_words = nltk.pos_tag(t_sentence)
    select_words = [(word,tag) for word,tag in tags_words if tag.startswith('NN') or 
        tag.startswith('VB')]
    return select_words

def lemmatize_word(word):
    lemma = WordNetLemmatizer()
    return lemma.lemmatize(word)

